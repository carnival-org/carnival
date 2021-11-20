import typing

from paramiko.client import SSHClient

from fabric.connection import Connection as FabricConnection  # type: ignore
from carnival.host.connection import Connection, Result


class _SSHConnection(Connection):
    def __init__(self, c: FabricConnection):
        self.c = c

    def run(self, command: str, hide: bool = False, pty: bool = False) -> Result:
        return self.c.run(command, hide=hide, pty=pty)  # type: ignore

    def open_shell(self, shell_cmd: typing.Optional[str] = None, cwd: typing.Optional[str] = None) -> None:
        # TODO: set shell_smd and cwd
        paramiko_client: SSHClient = self.c.client
        paramiko_client.invoke_shell()
