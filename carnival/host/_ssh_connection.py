import typing
from contextlib import contextmanager

from paramiko.client import SSHClient

from fabric.connection import Connection as FabricConnection  # type: ignore
from carnival.host.connection import Connection, Result, StatResult


class SSHConnection(Connection):
    def __init__(self, c: FabricConnection, sudo: bool):
        self.c = c
        self.paramiko_client: SSHClient = self.c.client
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

    def open_shell(self, shell_cmd: typing.Optional[str] = None, cwd: typing.Optional[str] = None) -> None:
        # TODO: get remote shell_cmd
        if shell_cmd is None:
            shell_cmd = "/bin/bash"

        self.run(shell_cmd, hide=False, sudo=self.sudo, cwd=cwd)

    def file_stat(self, path: str) -> StatResult:
        with self.paramiko_client.open_sftp() as sftp:

            stat = sftp.stat(path)
            assert stat.st_mode is not None
            assert stat.st_size is not None
            assert stat.st_uid is not None
            assert stat.st_gid is not None
            assert stat.st_atime is not None

            return StatResult(
                st_mode=stat.st_mode,
                st_size=stat.st_size,
                st_uid=stat.st_uid,
                st_gid=stat.st_gid,
                st_atime=stat.st_atime,
            )

    @contextmanager
    def file_read(self, path: str) -> typing.Generator[typing.IO[bytes], None, None]:
        with self.paramiko_client.open_sftp() as sftp:
            with sftp.open(path, 'rb') as reader:
                typed_reader = typing.cast(typing.IO[bytes], reader)
                yield typed_reader

    @contextmanager
    def file_write(self, path: str) -> typing.Generator[typing.IO[bytes], None, None]:
        with self.paramiko_client.open_sftp() as sftp:
            with sftp.open(path, 'wb') as writer:
                typed_writer = typing.cast(typing.IO[bytes], writer)
                yield typed_writer
