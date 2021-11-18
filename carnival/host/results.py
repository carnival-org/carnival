import typing


class _IOFileLike(typing.Protocol):
    def read(self, n: int = -1) -> bytes: ...
    def write(self, data: typing.Any) -> typing.Any: ...
    def close(self) -> None: ...


class Result:
    """
    Результат выполнения команды
    """

    def __init__(
        self,
        stdin: _IOFileLike,
        stdout: _IOFileLike,
        stderr: _IOFileLike,
        returncode: int,
    ) -> None:
        self.stdin = stdin  #: stdin
        self.stdout = stdout  #: stdout
        self.stderr = stderr  #: stderr
        self.returncode = returncode  #: код возврата команды

    def __del__(self) -> None:
        self.stdin.close()
        self.stdout.close()
        self.stderr.close()

    @property
    def ok(self) -> bool:
        """
        Команда была выполнена успешно
        """
        return self.returncode == 0


class ResultPromise():
    stdin: _IOFileLike
    stdout: _IOFileLike
    stderr: _IOFileLike
    bufsize: int = 1
    hide: bool

    def wait(self) -> Result:
        """
        Дождаться завершения команды
        """
        raise NotImplementedError

    def is_done(self) -> bool:
        """
        Команда была завершена
        """
        raise NotImplementedError
