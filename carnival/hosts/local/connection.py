import typing
import os

from carnival.hosts.base.connection import Connection
from carnival.hosts.base.stat_result import StatResult

from .result_promise import LocalResultPromise


class LocalConnection(Connection):
    def __enter__(self) -> Connection:
        return self

    def __exit__(self, *args: typing.Any) -> None:
        pass

    def run_promise(
            self,
            command: str,
            use_sudo: bool,
            env: typing.Optional[typing.Dict[str, str]] = None,
            cwd: typing.Optional[str] = None,
            timeout: int = 60,
    ) -> LocalResultPromise:
        return LocalResultPromise(
            command=command,
            cwd=cwd,
            env=env,
            use_sudo=use_sudo,
            timeout=timeout,
        )

    def file_stat(self, path: str) -> StatResult:
        stat = os.stat(path)
        return StatResult(
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
