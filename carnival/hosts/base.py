import typing
import ipaddress
import socket
import abc
from dataclasses import dataclass


class CommandError(BaseException):
    pass


class Result:
    """
    Результат выполнения команды
    """

    def __init__(
        self,
        return_code: int,
        stderr: str,
        stdout: str,

        command: str,
        hide: bool,
        warn: bool,
    ):
        """
        :param return_code: код возврата
        :param output: комбинированный вывод stdout & stderr
        :param command: команда, которая была запущена
        :param hide: не показывать вывод в консоли
        :param warn: вывести результат неуспешной команды вместо того чтобы выкинуть исключение :py:exc:`.CommandError`
        """
        self.return_code = return_code
        self.stderr = stderr.strip()
        self.stdout = stdout.strip()

        if not self.ok or len(self.stderr):
            if not warn:
                if self.stderr:
                    print(stderr)
                raise CommandError(f"{command} failed with exist code: {return_code}")

        if not hide:
            print(self.stdout)

    @property
    def ok(self) -> bool:
        return self.return_code == 0


@dataclass
class StatResult:
    st_mode: int
    st_size: int
    st_uid: int
    st_gid: int
    st_atime: float


class Connection:
    host: "Host"
    """
    Хост с которым связан конект
    """

    def __init__(self, host: "Host", run_timeout: int = 120) -> None:
        """
        Конекст с хостом, все конекты являются контекст-менеджерами

        >>> with host.connect() as c:
        >>>    c.run("ls -1")

        """
        self.host = host
        self.run_timeout = run_timeout

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

    @abc.abstractmethod
    def file_stat(self, path: str) -> StatResult:
        """
        Получить fstat файла

        :param path:  путь до файла
        """

    @abc.abstractmethod
    def file_read(self, path: str) -> typing.ContextManager[typing.IO[bytes]]:
        """
        Открыть файл на чтение

        :param path: путь до файла
        :return: дескриптор файла
        """

    @abc.abstractmethod
    def file_write(self, path: str) -> typing.ContextManager[typing.IO[bytes]]:
        """
        Открыть файл на запись

        :param path: путь до файла
        :return: дескриптор файла
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
