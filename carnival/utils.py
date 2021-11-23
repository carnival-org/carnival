from typing import Any, Optional, Protocol

from carnival import connection


class _Writer(Protocol):
    def write(self, __s: str) -> Any: ...


def log(message: str, file: Optional[_Writer] = None) -> None:
    if connection.host is None:
        host = "NO CONNECTION"
    else:
        host = str(connection.host)

    print(f"💃💃💃 {host}> {message}", file=file)
