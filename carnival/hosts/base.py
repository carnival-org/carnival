import typing
import ipaddress
import socket
import abc
from dataclasses import dataclass
from invoke.context import Result as InvokeResult  # type: ignore


@dataclass
class Result:
    """
    Результат выполнения команды
    """

    return_code: int
    ok: bool
    stdout: str
    stderr: str

    @classmethod
    def from_invoke_result(cls, invoke_result: InvokeResult) -> "Result":
        return Result(
            return_code=invoke_result.exited,
            ok=invoke_result.ok,
            stdout=invoke_result.stdout.replace("\r", ""),
            stderr=invoke_result.stderr.replace("\r", ""),
        )


class Connection:
    host: "Host"
    """
    Хост с которым связан конект
    """

    def __init__(self, host: "Host") -> None:
        """
        Конекст с хостом, все конекты являются контекст-менеджерами

        >>> with host.connect() as c:
        >>>    c.run("ls -1")

        """
        self.host = host

    def __enter__(self) -> "Connection":
        raise NotImplementedError

    def __exit__(self, *args: typing.Any) -> None:
        pass

    @abc.abstractmethod
    def run(
        self,
        command: str,
        hide: bool = False,
        warn: bool = False,
        cwd: typing.Optional[str] = None,
    ) -> Result:
        """
        Запустить команду

        :param command: Команда для запуска
        :param hide: Скрыть вывод команды
        :param warn: Вывести stderr
        :param cwd: Перейти в папку при выполнении команды
        """


class Host:
    addr: str = ""
    """
    Адрес хоста
    """

    @property
    def ip(self) -> str:
        # Maybe self.addr is ip?
        try:
            ip_obj: typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address] = ipaddress.ip_address(self.addr)
            return ip_obj.__str__()
        except ValueError:
            # Not ip
            pass

        # Maybe hostname?
        try:
            return socket.gethostbyname(self.addr)
        except socket.gaierror:
            # No ;(
            pass

        # TODO: maybe addr is ~/.ssh/config section?

        raise ValueError("cant get host ip")

    @abc.abstractmethod
    def connect(self) -> Connection:
        """
        Создать конект с хостом
        """
        ...

    def __str__(self) -> str:
        return f"🖥 {self.addr}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.addr}>"
