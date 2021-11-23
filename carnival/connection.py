from typing import Any, Optional, Type, Union

from fabric import Connection  # type:ignore
from invoke import Context  # type:ignore

from carnival.host import AnyHost
from carnival.exceptions import GlobalConnectionError


# noinspection PyTypeChecker
conn: Union[Connection, Context, None] = None
# noinspection PyTypeChecker
host: Optional[AnyHost] = None


class SetConnection:
    def __init__(self, h: AnyHost):
        self.host = h

    def __enter__(self) -> None:
        global conn
        global host

        if host is not None:
            raise GlobalConnectionError(f"Cannot set context, while other context active: {host}")
        if conn is not None:
            raise GlobalConnectionError(f"Cannot set context, while other context active: {conn}")

        conn = self.host.connect()
        host = self.host

    def __exit__(self, exc_type: Type[Any], exc_val: Any, exc_tb: Any) -> None:
        global conn
        global host
        conn = None
        host = None
