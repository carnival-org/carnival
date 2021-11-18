from types import TracebackType
import typing
import io
from subprocess import Popen, PIPE

from carnival.host import _base
from carnival.host import results


class ResultPromise(results.ResultPromise):
    def __init__(self, command: str, hide: bool):
        if hide:
            self._proc = Popen(command, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE)
            assert self._proc.stdin is not None
            assert self._proc.stdout is not None
            assert self._proc.stderr is not None

            self.stdin = self._proc.stdin
            self.stdout = self._proc.stdout
            self.stderr = self._proc.stderr
        else:
            self._proc = Popen(command, shell=True)
            self._proc.communicate()

            self.stdin = io.BytesIO()
            self.stdout = io.BytesIO()
            self.stderr = io.BytesIO()

    def is_done(self) -> bool:
        return self._proc.poll() is not None

    def wait(self) -> results.Result:
        returncode = self._proc.wait()

        return results.Result(
            returncode=returncode,
            stderr=self.stderr,
            stdin=self.stdin,
            stdout=self.stdout
        )


class LocalConnection(_base.ConnectionBase):
    def run(self, command: str, hide: bool) -> ResultPromise:
        """
        Выполнить команду

        :param command: команда
        :param hide: скрыть вывод
        """
        return ResultPromise(command, hide=hide)

    def __enter__(self) -> "LocalConnection":
        return self

    def __exit__(self, exc_type: typing.Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        pass


class LocalHost(_base.HostBase):
    def connect(self) -> LocalConnection:
        return LocalConnection()

    def get_address(self) -> str:
        return "localhost"


localhost = LocalHost()  #: Инстанс окалхоста, синглтон

__all__ = [
    'LocalConnection',
    'LocalHost',
    'localhost',
]
