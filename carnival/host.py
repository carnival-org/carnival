from typing import Union, Optional

from fabric import Connection  # type: ignore
from invoke import Context  # type: ignore

LOCAL_ADDRS = [
    'local',
    'localhost',
]


class Host:
    """
    Объект, представляющий единицу оборудования.

    Carnival не предоставляет никаких сложных абстракций для работы с группами хостов,
    подразумевая что вы будете использовать встроенные коллекции python и организуете
    работу так, как будет удобно для вашей задачи.

    >>> class SetupFrontend(Task):
    >>>    def run(self, **kwargs):
    >>>        self.step(Frontend(), Host("1.2.3.4", packages=["htop", ]))

    В более сложных, создать списки в файле `inventory.py`

    >>> # inventory.py
    >>> frontends = [
    >>>     Host("1.2.3.4"),
    >>>     Host("1.2.3.5"),
    >>> ]

    >>> # carnival_tasks.py
    >>> import inventory as i
    >>> class SetupFrontend(Task):
    >>>    def run(self, **kwargs):
    >>>        self.step(Frontend(), i.frontends)


    """
    def __init__(
        self,
        addr: str,
        ssh_user: str = None, ssh_password: str = None, ssh_port=22,
        ssh_gateway: Optional['Host'] = None,
        ssh_connect_timeout: int = 10,

        **context
     ):
        """
        В простом случае, можно передавать хосты прямо в коде файла `carnival_tasks.py`.

        :param addr: Адрес сервера
        :param ssh_user: Пользователь SSH
        :param ssh_password: Пароль SSH
        :param ssh_port: SSH порт
        :param ssh_connect_timeout: SSH таймаут соединения
        :param ssh_gateway: Gateway
        :param context: Контекст хоста
        """
        self.addr = addr
        self.ssh_port = ssh_port
        self.context = context
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout
        self.ssh_gateway: Optional['Host'] = ssh_gateway

    def is_connection_local(self) -> bool:
        """
        Check if host's connection is local
        """
        return self.host.lower() in LOCAL_ADDRS

    def connect(self) -> Union[Connection, Context]:
        if self.is_connection_local():
            # Host is local machine
            return Context()
        else:
            # Host is remote ssh machine

            gateway = None
            if self.ssh_gateway:
                gateway = self.ssh_gateway.connect()
                assert isinstance(gateway, Connection), f"{self.ssh_gateway} is not ssh connection"

            return Connection(
                host=self.addr,
                port=self.ssh_port,
                user=self.ssh_user,
                connect_timeout=self.ssh_connect_timeout,
                gateway=gateway,
                connect_kwargs={
                    'password': self.ssh_password,
                }
            )

    @property
    def host(self) -> str:
        """
        Remove user and port parts, return just address
        """

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

    def __repr__(self):
        return f"<Host object {self.host}>"
