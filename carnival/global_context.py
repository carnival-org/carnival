from typing import Union

from fabric import Connection
from invoke import Context

from carnival.host import Host


# noinspection PyTypeChecker
conn: Union[Connection, Context] = None
# noinspection PyTypeChecker
host: Host = None


def set_context(h: Host):
    global conn
    global host
    conn = h.connect()
    host = h
