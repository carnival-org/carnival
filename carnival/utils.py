from typing import Any, Optional, Protocol

from carnival import global_context


class _Writer(Protocol):
    def write(self, __s: str) -> Any: ...


def log(message: str, file: Optional[_Writer] = None) -> None:
    if global_context.host is None:
        host = "NO CONNECTION"
    else:
        host = global_context.host.host

    print(f"💃💃💃 {host}> {message}", file=file)
