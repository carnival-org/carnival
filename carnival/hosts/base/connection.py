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

    tempdir = "/tmp"

    def __init__(self, host: "Host", use_sudo: bool = False) -> None:
        """
        Конекст с хостом, все конекты являются контекст-менеджерами

        >>> with host.connect() as c:
        >>>    c.run("ls -1")

        :param host: хост с которым связано соединение
        :param use_sudo: использовать sudo для выполнения команд
        """
        self.host = host
        self.use_sudo = use_sudo

    def __enter__(self) -> "Connection":
        raise NotImplementedError

    def __exit__(self, *args: typing.Any) -> None:
        pass

    @abc.abstractmethod
    def run_promise(
        self,
        command: str,
        use_sudo: bool,
        env: typing.Optional[typing.Dict[str, str]] = None,
        cwd: typing.Optional[str] = None,
        timeout: int = 60,
    ) -> ResultPromise:
        raise NotImplementedError

    def run(
        self,
        command: str,
        use_sudo: typing.Optional[bool] = None,
        env: typing.Optional[typing.Dict[str, str]] = None,
        hide: bool = True,
        show_command: bool = False,
        warn: bool = False,
        cwd: typing.Optional[str] = None,
        timeout: int = 60,
    ) -> Result:
        """
        Запустить команду

        :param command: Команда для запуска
        :param use_sudo: использовать sudo для выполнения команды, если не задано используется значение `self.use_sudo`
        :param env: задать переменные окружения для команды
        :param hide: Скрыть вывод команды
        :param show_command: показать исполняемую команду
        :param warn: Вывести stderr
        :param cwd: Перейти в папку при выполнении команды
        :param timeout: таймаут выполнения команды
        """

        if use_sudo is None:
            use_sudo = self.use_sudo

        result = self.run_promise(
            command=command,
            env=env,
            cwd=cwd,
            use_sudo=use_sudo,
            timeout=timeout,
        ).get_result(hide=hide, show_command=show_command)
        result.check_result(warn=warn, hide=hide)
        return result

    @abc.abstractmethod
    def file_stat(self, path: str) -> StatResult:
        """
        Получить fstat файла,
        не поддерживает `use_sudo`

        :param path:  путь до файла
        """

    @abc.abstractmethod
    def file_read(self, path: str) -> typing.ContextManager[typing.IO[bytes]]:
        """
        Открыть файл на чтение
        не поддерживает `use_sudo`

        :param path: путь до файла
        :return: дескриптор файла
        """

    @abc.abstractmethod
    def file_write(self, path: str) -> typing.ContextManager[typing.IO[bytes]]:
        """
        Открыть файл на запись
        не поддерживает `use_sudo`

        :param path: путь до файла
        :return: дескриптор файла
        """
