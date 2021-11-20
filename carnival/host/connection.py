import abc
import typing

from invoke.context import Result as InvokeResult  # type: ignore


class Result(InvokeResult):  # type: ignore
    exited: int


class Connection(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, command: str, hide: bool = False, pty: bool = False) -> Result: ...

    @abc.abstractmethod
    def open_shell(self, shell_cmd: typing.Optional[str] = None, cwd: typing.Optional[str] = None) -> None: ...
