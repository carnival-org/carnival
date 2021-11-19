import abc

from paramiko.client import SSHClient
from fabric.connection import Connection  # type: ignore
from invoke.context import Context, Result as InvokeResult  # type: ignore


class Result(InvokeResult):  # type: ignore
    exited: int


class AnyConnection(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, command: str, hide: bool = False, pty: bool = False) -> Result: ...


class LocalConnection(AnyConnection):
    def __init__(self) -> None:
        self.c = Context()

    def run(self, command: str, hide: bool = False, pty: bool = False) -> Result:
        return self.c.run(command, hide=hide, pty=pty)  # type: ignore


class SSHConnection(AnyConnection):
    def __init__(self, c: Connection):
        self.c = c

    def run(self, command: str, hide: bool = False, pty: bool = False) -> Result:
        return self.c.run(command, hide=hide, pty=pty)  # type: ignore

    def open_shell(self) -> None:
        paramiko_client: SSHClient = self.c.client
        paramiko_client.invoke_shell()


__all__ = (
    'Result',
    'AnyConnection',
    'LocalConnection',
    'SSHConnection',
)
