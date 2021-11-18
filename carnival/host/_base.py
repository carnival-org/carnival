from types import TracebackType
import typing

from carnival.host.results import ResultPromise


class ConnectionBase:
    def run(self, command: str, hide: bool) -> ResultPromise:
        raise NotImplementedError

    def __enter__(self) -> "ConnectionBase":
        raise NotImplementedError

    def __exit__(self, exc_type: typing.Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        raise NotImplementedError


ConnectionBaseT = typing.TypeVar("ConnectionBaseT", bound=ConnectionBase)


class HostBase:
    def connect(self) -> ConnectionBase:
        raise NotImplementedError

    def get_address(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"🖥 {self.get_address()}"

    def __hash__(self) -> int:
        return hash(self.get_address())

    def __repr__(self) -> str:
        return f"<Host object {self.get_address()}>"


HostBaseT = typing.TypeVar("HostBaseT", bound=HostBase)
