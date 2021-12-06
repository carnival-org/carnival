"""
Валидаторы для шагов
"""

import typing
import abc

from carnival.steps import _validator_cache, shortcuts
from carnival.templates import render
from carnival import localhost_connection

from jinja2.exceptions import UndefinedError, TemplateNotFound, TemplateSyntaxError


if typing.TYPE_CHECKING:
    from carnival import Connection


class StepValidatorBase:
    @abc.abstractmethod
    def validate(self, c: "Connection") -> typing.Optional[str]:
        """
        Реализация валидатора

        :param c: конект с хостом
        :return: строковое описание ошибки, либо `None`
        """
        raise NotImplementedError


class InlineValidator(StepValidatorBase):
    """
    lambda валидатор, удобен для создания валидатора на лету
    """
    def __init__(
        self,
        if_err_true_fn: typing.Callable[["Connection"], bool],
        error_message: str,
        fact_id_for_caching: typing.Optional[str] = None,
    ):
        """
        :param if_err_true_fn: фукнция проверки, должна вернуть `True` чтобы валидатор вернул ошибку
        :param error_message: сообщение об ошибке валидатора
        :param fact_id_for_caching: идентификатор факта для кеширования фактов, не используется если `None`
        """
        self.if_err_true_fn = if_err_true_fn
        self.error_message = error_message
        self.fact_id_for_caching = fact_id_for_caching

    def validate(self, c: "Connection") -> typing.Optional[str]:
        if self.fact_id_for_caching is not None:
            is_exist, val = _validator_cache.try_get(self.__class__, c.host, self.fact_id_for_caching)
            if is_exist:
                return val

        val = None
        if self.if_err_true_fn(c):
            val = self.error_message

        if self.fact_id_for_caching is not None:
            _validator_cache.set(self.__class__, c.host, self.fact_id_for_caching, val=val)
        return val


class CommandRequiredValidator(StepValidatorBase):
    """
    Проверяет что команда есть в $PATH

    >>> from carnival.steps import validators
    >>> ...
    >>> validators.CommandRequiredValidator('docker')
    """
    def __init__(self, command: str) -> None:
        """
        :param command: команда
        """
        self.command = command
        self.fact_id = f"path-{command}-required"

    def validate(self, c: "Connection") -> typing.Optional[str]:
        is_exist, val = _validator_cache.try_get(self.__class__, c.host, self.fact_id)

        if is_exist:
            return val

        val = None
        if not shortcuts.is_cmd_exist(c, self.command):
            val = f"'{self.command}' is required"

        _validator_cache.set(self.__class__, c.host, self.fact_id, val=val)
        return val


class IsFileValidator(StepValidatorBase):
    """
    Проверяет что обьект по заданному пути является файлом
    """
    def __init__(self, file_path: str) -> None:
        """
        :param file_path: путь до обьекта
        """
        self.file_path = file_path
        self.fact_id = f"isfile-{file_path}"

    def validate(self, c: "Connection") -> typing.Optional[str]:
        is_exist, val = _validator_cache.try_get(self.__class__, c.host, self.fact_id)

        if is_exist:
            return val

        val = None

        if not shortcuts.is_file(c, self.file_path):
            val = f"'{self.file_path}' is not file"

        _validator_cache.set(self.__class__, c.host, self.fact_id, val=val)
        return val


class IsDirectoryValidator(StepValidatorBase):
    """
    Проверяет что обьект по заданному пути является директорией
    """

    def __init__(self, directory_path: str) -> None:
        """
        :param directory_path: путь до директории
        """
        self.directory_path = directory_path
        self.fact_id = f"is_directory-{directory_path}"

    def validate(self, c: "Connection") -> typing.Optional[str]:
        is_exist, val = _validator_cache.try_get(self.__class__, c.host, self.fact_id)

        if is_exist:
            return val

        val = None

        if not shortcuts.is_directory(c, self.directory_path):
            val = f"'{self.directory_path}' is not directory"

        _validator_cache.set(self.__class__, c.host, self.fact_id, val=val)
        return val


class TemplateValidator(StepValidatorBase):
    """
    Валидатор шаблонов `carnival.templates`
    """
    def __init__(self, template_path: str, context: typing.Dict[str, typing.Any]):
        """
        :param template_path: путь до шаблона
        :param context: контекст шаблона
        """
        self.template_path = template_path
        self.context = context

    def validate(self, c: "Connection") -> typing.Optional[str]:
        # TODO: more catch errors maybe?
        try:
            render(self.template_path, **self.context)
        except (UndefinedError, TemplateNotFound, TemplateSyntaxError) as ex:
            return f"{ex.__class__.__name__}: {ex}"
        return None


class Not(StepValidatorBase):
    """
    Валидатор который принимает другой валидатор и инвертирует его ответ

    Валидатор, который провеяет что команды docker нет в $PATH

    >>> from carnival.steps import validators
    >>>
    >>>  Not(
    >>>      validator=CommandRequiredValidator("docker"),
    >>>      error_message="docker shoult not be exist"
    >>>  )
    """
    def __init__(
        self,
        validator: StepValidatorBase,
        error_message: str,
    ):
        """
        :param validator: валидатор
        :param error_message: сообщение об ошибке валидатора
        """

        self.validator = validator
        self.error_message = error_message

    def validate(self, c: "Connection") -> typing.Optional[str]:
        err = self.validator.validate(c)
        if err is None:
            return self.error_message
        return None


class Or(StepValidatorBase):
    """
    Валидатор который принимает список валидаторов и будет успешен если хотя бы один их них успешен
    """
    def __init__(
        self,
        validators: typing.List[StepValidatorBase],
        error_message: str,
    ):
        """
        :param validators: валидаторы
        :param error_message: сообщение об ошибке валидатора
        """

        self.validators = validators
        self.error_message = error_message

    def validate(self, c: "Connection") -> typing.Optional[str]:
        for v in self.validators:
            err = v.validate(c)
            if err is None:
                return None

        return self.error_message


class Local(StepValidatorBase):
    """
    Запускает проверку валидатор а на локальном хосте

    >>> from carnival.steps import validators
    >>> Local(CommandRequiredValidator("docker"))  # Проверяем наличие docker на локальном хосте
    """
    def __init__(
        self,
        validator: StepValidatorBase,
    ):
        """
        :param validator: валидатор
        """

        self.validator = validator

    def validate(self, c: "Connection") -> typing.Optional[str]:
        return self.validator.validate(localhost_connection)
