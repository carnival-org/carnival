import abc
import typing
import re

from carnival.host import Host


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


class Context(typing.Protocol):
    pass


ContextT = typing.TypeVar("ContextT", bound=Context)


class Step(typing.Generic[ContextT], metaclass=abc.ABCMeta):
    """
    Шаг - объект, предназначенный для выполнения группы комманд с какой-то целью.
    Вызывается из класса `carnival.Task` для выполнения комманд (`carnival.cmd`) на определенных хостах.

    Может требовать наличие определенных контекстных переменных для работы, указав их в аргументах метода `run`.
    Может вернуть значение для дальнейшего использования.

    В следующем примере переменная обьявлен шаг для установки

    >>> class PackagesContextProtocol(typing.Protocol):
    >>>     packages: typing.List[str]
    >>>
    >>>
    >>> PackagesContextProtocolT = typing.TypeVar("PackagesContextProtocolT", bound=PackagesContextProtocol)
    >>>
    >>>
    >>> class AptInstall(Step[PackagesContextProtocolT]):
    >>>     def run(self) -> None:
    >>>         with self.host.connect():
    >>>             result = cmd.apt.install_multiple(self.host.context.packages)
    >>>             if self.print_result:
    >>>                 print(result)

    """

    def __init__(self, host: Host[ContextT]) -> None:
        self.host = host

    @abc.abstractmethod
    def run(self) -> None:
        print(f"💃💃💃 Running {_underscore(self.__class__.__name__)} at {self.host}")
