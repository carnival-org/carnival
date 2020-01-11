from typing import Union, Dict, Any

from fabric import Connection
from invoke import Context

from carnival.host import Host

# noinspection PyTypeChecker
conn: Union[Connection, Context] = None
# noinspection PyTypeChecker
host: Host = None
context: Dict[str, Any] = {}
secrets: Dict[str, Any] = {}
