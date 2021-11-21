import abc
import typing
from dataclasses import dataclass

from invoke.context import Result as InvokeResult  # type: ignore


@dataclass
class Result:
    return_code: int
    ok: bool
    stdout: str
    stderr: str

    @classmethod
    def from_invoke_result(cls, invoke_result: InvokeResult) -> "Result":
        return Result(
            return_code=invoke_result.exited,
            ok=invoke_result.ok,
            stdout=invoke_result.stdout,
            stderr=invoke_result.stderr,
        )


@dataclass
class StatResult:
    st_mode: int
    st_size: int
    st_uid: int
    st_gid: int
    st_atime: float


class Connection(metaclass=abc.ABCMeta):
    def __init__(self, sudo: bool) -> None:
        self.sudo = sudo

    @abc.abstractmethod
    def run(
        self,
        command: str,
        hide: bool = False, warn: bool = True, cwd: typing.Optional[str] = None, sudo: typing.Optional[bool] = None,
    ) -> Result: ...

    @abc.abstractmethod
    def open_shell(
        self,
        shell_cmd: typing.Optional[str] = None,
        cwd: typing.Optional[str] = None, sudo: typing.Optional[bool] = None,
    ) -> None: ...

    @abc.abstractmethod
    def file_stat(self, path: str, sudo: typing.Optional[bool] = None,) -> StatResult: ...

    @abc.abstractmethod
    def file_read(self, path: str, sudo: typing.Optional[bool] = None,) -> typing.ContextManager[typing.IO[bytes]]: ...

    @abc.abstractmethod
    def file_write(self, path: str, sudo: typing.Optional[bool] = None,) -> typing.ContextManager[typing.IO[bytes]]: ...
