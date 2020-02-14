from typing import Union

from fabric import Connection  # type:ignore
from invoke import Context  # type:ignore

from carnival.host import Host


# noinspection PyTypeChecker
conn: Union[Connection, Context] = None
# noinspection PyTypeChecker
host: Host = None  # type:ignore


class SetContext:
    def __init__(self, h: Host):
        self.host = h

    def __enter__(self):
        global conn
        global host

        assert host is None, f"Cannot set context, while other context active: {host}"
        assert conn is None, f"Cannot set context, while other context active: {conn}"

        conn = self.host.connect()
        host = self.host

    def __exit__(self, exc_type, exc_val, exc_tb):
        global conn
        global host
        conn = None
        host = None
