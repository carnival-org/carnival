from typing import Union, Dict, Any
import abc

from fabric import Connection
from invoke import Context

LOCAL_ADDRS = [
    'local',
    'localhost',
]


class HostBase(abc.ABC):
    addr: str
    context: Dict[str, Any]

    def connect(self) -> Union[Connection, Context]:
        if self.addr in LOCAL_ADDRS:
            # Host is local machine
            return Context()
        else:
            # Host is remote ssh machine
            return Connection(self.addr, connect_timeout=10)

    def __str__(self):
        return f"🖥 {self.addr}"

    def __hash__(self):
        return hash(self.addr)
