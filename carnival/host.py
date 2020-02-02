from typing import Union

from fabric import Connection  # type: ignore
from invoke import Context  # type: ignore

LOCAL_ADDRS = [
    'local',
    'localhost',
]


class Host:
    def __init__(
        self,
        addr: str,
        ssh_user: str = None, ssh_password: str = None, ssh_port=22,
        ssh_connect_timeout: int = 10,
        **context
     ):
        """
        Defined host to operate in
        :param addr: user@host, host, ip for remote, one if LOCAL_ADDRS for local execution
        :param context: Some context vars for use in runtime
        """
        self.addr = addr
        self.ssh_port = ssh_port
        self.context = context
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout

    def is_connection_local(self):
        return self.host.lower() in LOCAL_ADDRS

    def connect(self) -> Union[Connection, Context]:
        if self.is_connection_local():
            # Host is local machine
            return Context()
        else:
            # Host is remote ssh machine
            return Connection(
                host=self.addr,
                port=self.ssh_port,
                user=self.ssh_user,
                connect_timeout=self.ssh_connect_timeout,
                connect_kwargs={
                    'password': self.ssh_password,
                }
            )

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
        return f"🖥 {self.host}"

    def __hash__(self):
        return hash(self.addr)
