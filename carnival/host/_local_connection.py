
import typing
import os

from invoke.context import Context  # type: ignore

from carnival.host.connection import Connection, Result, StatResult


class LocalConnection(Connection):
    def __init__(self, sudo: bool) -> None:
        self.c = Context()
        super().__init__(sudo=sudo)

    def run(
        self,
        command: str,
        hide: bool = False, warn: bool = True, cwd: typing.Optional[str] = None, sudo: typing.Optional[bool] = None,
    ) -> Result:
        if sudo is None:
            sudo = self.sudo
        assert sudo is not None

        handler_kwargs = {
            "command": command,
            "hide": hide,
            "pty": True,
            "warn": warn,
        }

        handler = self.c.run
        if sudo is True:
            handler = self.c.sudo

        if cwd is not None:
            with self.c.cd(cwd):
                return Result.from_invoke_result(handler(**handler_kwargs))

        return Result.from_invoke_result(handler(**handler_kwargs))

    def open_shell(
        self,
        shell_cmd: typing.Optional[str] = None,
        cwd: typing.Optional[str] = None, sudo: typing.Optional[bool] = None,
    ) -> None:
        if sudo is None:
            sudo = self.sudo
        assert sudo is not None

        if shell_cmd is None:
            shell_cmd = os.getenv("SHELL", '/bin/sh')

        assert shell_cmd is not None
        self.run(shell_cmd, hide=False, sudo=sudo, cwd=cwd)

    def file_stat(self, path: str, sudo: typing.Optional[bool] = None) -> StatResult:
        if sudo is None:
            sudo = self.sudo
        assert sudo is not None

        if sudo is True:
            # TODO: handle sudo
            raise NotImplementedError

        stat = os.stat(path)
        return StatResult(
            st_mode=stat.st_mode,
            st_size=stat.st_size,
            st_uid=stat.st_uid,
            st_gid=stat.st_gid,
            st_atime=stat.st_atime,
        )

    def file_read(self, path: str, sudo: typing.Optional[bool] = None) -> typing.ContextManager[typing.IO[bytes]]:
        if sudo is None:
            sudo = self.sudo
        assert sudo is not None

        if sudo is True:
            # TODO: handle sudo
            raise NotImplementedError

        return open(path, 'rb')

    def file_write(self, path: str, sudo: typing.Optional[bool] = None) -> typing.ContextManager[typing.IO[bytes]]:
        if sudo is None:
            sudo = self.sudo
        assert sudo is not None

        if sudo is True:
            # TODO: handle sudo
            raise NotImplementedError

        return open(path, 'wb')
