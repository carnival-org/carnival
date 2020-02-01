from typing import Union

from fabric import Connection  # type:ignore
from invoke import Context  # type:ignore

from carnival.host import Host


# noinspection PyTypeChecker
conn: Union[Connection, Context] = None
# noinspection PyTypeChecker
host: Host = None  # type:ignore


def set_context(h: Host):
    global conn
    global host
    conn = h.connect()
    host = h
