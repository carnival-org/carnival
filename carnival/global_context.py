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

    assert host is None, f"Cannot set context, while other context active: {host}"
    assert conn is None, f"Cannot set context, while other context active: {conn}"

    conn = h.connect()
    host = h


def flush_context():
    global conn
    global host
    conn = None
    host = None
