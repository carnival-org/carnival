import typing
import os
from subprocess import Popen, PIPE

from carnival.hosts import base


class LocalResultPromise(base.ResultPromise):
    def __init__(
            self,
            command: str,
            timeout: int,
            cwd: typing.Optional[str]
    ):
        self.proc = Popen(command, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE, cwd=cwd)
        self.command = command
        assert self.proc.stdout is not None
        assert self.proc.stderr is not None
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        self.timeout = timeout

    def is_done(self) -> bool:
        return self.proc.poll() is not None

    def wait(self) -> int:
        return self.proc.wait(timeout=self.timeout)

    def get_result(self, hide: bool) -> base.Result:
        result = super().get_result(hide=hide)
        self.proc.__exit__(None, None, None)
        return result


class LocalConnection(base.Connection):
    def __enter__(self) -> base.Connection:
        return self

    def __exit__(self, *args: typing.Any) -> None:
        pass

    def run_promise(
        self,
        command: str,
        cwd: typing.Optional[str] = None,
        timeout: int = 60,
    ) -> LocalResultPromise:
        return LocalResultPromise(
            command=command,
            cwd=cwd,
            timeout=timeout,
        )

    def file_stat(self, path: str) -> base.StatResult:
        stat = os.stat(path)
        return base.StatResult(
            st_mode=stat.st_mode,
            st_size=stat.st_size,
            st_uid=stat.st_uid,
            st_gid=stat.st_gid,
            st_atime=stat.st_atime,
        )

    def file_read(self, path: str) -> typing.ContextManager[typing.IO[bytes]]:
        return open(path, 'rb')

    def file_write(self, path: str) -> typing.ContextManager[typing.IO[bytes]]:
        return open(path, 'wb')


class LocalHost(base.Host):
    """
    Локальный хост, работает по локальному терминалу
    """

    addr: str = "localhost"
    """
    Адрес хоста, всегда `localhost`
    """

    def connect(self) -> LocalConnection:
        return LocalConnection(host=self)


localhost = LocalHost()
localhost_connection = localhost.connect().__enter__()
