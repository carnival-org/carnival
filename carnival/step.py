import abc
import typing

from carnival.host import Host


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
    >>>     def __init__(self, print_result=False):
    >>>         self.print_result = print_result
    >>>
    >>>     def run(self) -> None:
    >>>         with host.connect():
    >>>             result = cmd.apt.install_multiple(host.context.packages)
    >>>             if self.print_result:
    >>>                 print(result)

    """

    def __init__(self, host: Host[ContextT]):
        self.host: Host[ContextT] = host

    @abc.abstractmethod
    def run(self) -> None: ...
