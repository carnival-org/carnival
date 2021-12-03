import typing
import abc

from carnival import cmd
from carnival.steps import _validator_cache
from carnival.templates import render

from jinja2.exceptions import UndefinedError, TemplateNotFound, TemplateSyntaxError


if typing.TYPE_CHECKING:
    from carnival import Connection
    from carnival.steps.step import Step


class StepValidatorBase:
    def __init__(self, step: "Step"):
        self.step = step

    @abc.abstractmethod
    def validate(self, c: "Connection") -> typing.Optional[str]:
        raise NotImplementedError


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
        if not cmd.cli.is_cmd_exist(c, self.command):
            val = f"'{self.command}' is required"

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
