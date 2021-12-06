import typing
import os
from subprocess import Popen, PIPE

from carnival.hosts import base


class LocalConnection(base.Connection):
    def __enter__(self) -> base.Connection:
        return self

    def __exit__(self, *args: typing.Any) -> None:
        pass

    def run(
        self,
        command: str,
        hide: bool = False,
        warn: bool = False,
        cwd: typing.Optional[str] = None,
    ) -> base.Result:
        with Popen(command, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE, cwd=cwd) as proc:
            retcode = proc.wait(timeout=self.run_timeout)

            assert proc.stdout is not None
            assert proc.stderr is not None

            return base.Result(
                return_code=retcode,
                stdout=proc.stdout.read().decode().replace("\r", ""),
                stderr=proc.stderr.read().decode().replace("\r", ""),

                command=command,
                hide=hide,
                warn=warn,
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
