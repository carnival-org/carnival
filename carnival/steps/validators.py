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
        raise NotImplementedError


class Not(StepValidatorBase):
    def __init__(
        self,
        validator: StepValidatorBase,
        error_message: str,
    ):
        self.validator = validator
        self.error_message = error_message

    def validate(self, c: "Connection") -> typing.Optional[str]:
        err = self.validator.validate(c)
        if err is None:
            return self.error_message
        return None


class InlineValidator(StepValidatorBase):
    def __init__(
        self,
        if_err_true_fn: typing.Callable[["Connection"], bool],
        error_message: str,
        fact_id_for_caching: typing.Optional[str] = None,
    ):
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
    def __init__(self, command: str) -> None:
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
    def __init__(self, file_path: str, on_localhost: bool = False) -> None:
        self.file_path = file_path
        self.on_localhost = on_localhost

        self.fact_id = f"isfile-{file_path}"

    def validate(self, c: "Connection") -> typing.Optional[str]:
        if self.on_localhost:
            c = localhost_connection

        is_exist, val = _validator_cache.try_get(self.__class__, c.host, self.fact_id)

        if is_exist:
            return val

        val = None

        if not shortcuts.is_file(c, self.file_path):
            val = f"'{self.file_path}' is not file"

        _validator_cache.set(self.__class__, c.host, self.fact_id, val=val)
        return val


class IsDirectoryValidator(StepValidatorBase):
    def __init__(self, directory_path: str, on_localhost: bool = False) -> None:
        self.directory_path = directory_path
        self.on_localhost = on_localhost

        self.fact_id = f"is_directory-{directory_path}"

    def validate(self, c: "Connection") -> typing.Optional[str]:
        if self.on_localhost:
            c = localhost_connection

        is_exist, val = _validator_cache.try_get(self.__class__, c.host, self.fact_id)

        if is_exist:
            return val

        val = None

        if not shortcuts.is_directory(c, self.directory_path):
            val = f"'{self.directory_path}' is not directory"

        _validator_cache.set(self.__class__, c.host, self.fact_id, val=val)
        return val


class TemplateValidator(StepValidatorBase):
    def __init__(self, template_path: str, context: typing.Dict[str, typing.Any]):
        self.template_path = template_path
        self.context = context

    def validate(self, c: "Connection") -> typing.Optional[str]:
        # TODO: more catch errors maybe?
        try:
            render(self.template_path, **self.context)
        except (UndefinedError, TemplateNotFound, TemplateSyntaxError) as ex:
            return f"{ex.__class__.__name__}: {ex}"
        return None
