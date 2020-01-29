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

    @property
    def host(self) -> str:
        # Remove user and port parts

        h = self.addr
        if '@' in self.addr:
            h = h.split("@", maxsplit=1)[1]

        if ':' in self.addr:
            h = h.split(":", maxsplit=1)[0]

        return h

    def __str__(self):
        return f"🖥 {self.addr}"

    def __hash__(self):
        return hash(self.addr)
