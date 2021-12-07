import typing
import abc

from .result import Result
from .result_promise import ResultPromise
from .stat_result import StatResult


if typing.TYPE_CHECKING:
    from .host import Host


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
    def run_promise(
            self,
            command: str,
            cwd: typing.Optional[str] = None,
            timeout: int = 60,
    ) -> ResultPromise:
        raise NotImplementedError

    def run(
            self,
            command: str,
            hide: bool = True,
            warn: bool = False,
            cwd: typing.Optional[str] = None,
            timeout: int = 60,
    ) -> Result:
        """
        Запустить команду

        :param command: Команда для запуска
        :param hide: Скрыть вывод команды
        :param warn: Вывести stderr
        :param cwd: Перейти в папку при выполнении команды
        :param timeout: таймаут выполнения команды
        """
        result = self.run_promise(
            command=command,
            cwd=cwd,
            timeout=timeout,
        ).get_result(hide=hide)
        result.check_result(warn=warn)
        return result

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
