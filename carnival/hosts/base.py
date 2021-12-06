import io
from threading import Thread
import sys
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
    ) -> None:
        """
        :param return_code: код возврата
        :param stderr: содержимое stderr
        :param stdout: содержимое stdout
        :param command: команда, которая была запущена

        """
        self.command = command
        self.return_code = return_code
        self.stderr = stderr.replace("\r", "").strip()
        self.stdout = stdout.replace("\r", "").strip()

    def check_result(self, warn: bool) -> None:
        """
        Проверить результат выполнения, выкинуть ошибку если она была

        :param warn: вывести результат неуспешной команды вместо того чтобы выкинуть исключение :py:exc:`.CommandError`
        """
        if not self.ok or len(self.stderr):
            if self.stdout:
                print(self.stdout, flush=True)
            if self.stderr:
                print(self.stderr, flush=True)

            if not warn:
                raise CommandError(f"{self.command} failed with exist code: {self.return_code}")

    @property
    def ok(self) -> bool:
        return self.return_code == 0


class ResultPromise:
    command: str
    stdout: typing.IO[bytes]
    stderr: typing.IO[bytes]

    @abc.abstractmethod
    def is_done(self) -> bool: ...

    @abc.abstractmethod
    def wait(self) -> int: ...

    def get_result(self, hide: bool) -> Result:
        """
        Получить результат

        :param hide: скрыть stdin & stdout
        """
        if hide is True:
            retcode = self.wait()
            return Result(
                return_code=retcode,
                stderr=self.stderr.read().decode(),
                stdout=self.stdout.read().decode(),
                command=self.command,
            )

        # Копируем stdout & stderr команды на экран и в буферы
        # чтобы вернуть результат
        threads = []

        cmd_stdout = io.BytesIO()
        cmd_stderr = io.BytesIO()

        def output_thread(fromio: typing.IO[bytes], toios: typing.List[typing.IO[bytes]]) -> None:
            while not self.is_done():
                data = fromio.read(1)
                for toio in toios:
                    toio.write(data)
                    toio.flush()

            data = fromio.read()
            for toio in toios:
                toio.write(data)
                toio.flush()

        threads.append(Thread(target=output_thread, args=(self.stdout, [sys.stdout.buffer, cmd_stdout])))
        # threads.append(Thread(target=output_thread, args=(self.stderr, [sys.stderr.buffer, cmd_stderr])))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        cmd_stdout.seek(0)
        cmd_stderr.seek(0)

        retcode = self.wait()
        return Result(
            return_code=retcode,
            stderr=cmd_stderr.read().decode(),
            stdout=cmd_stdout.read().decode(),
            command=self.command,
        )


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
