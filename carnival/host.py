"""
Объект, представляющий единицу оборудования.

Carnival не предоставляет никаких сложных абстракций для работы с группами хостов,
подразумевая что вы будете использовать встроенные коллекции python и организуете
работу так, как будет удобно для вашей задачи.
В простом случае, можно передавать хосты прямо в коде файла `carnival_tasks.py`.

>>> class SetupFrontend(Task):
>>>    def run(self, **kwargs):
>>>        self.step(Frontend(), SSHHost("1.2.3.4", packages=["htop", ]))

В более сложных, создать списки в файле `inventory.py`

>>> # inventory.py
>>> frontends = [
>>>     LocalHost(),
>>>     SSHHost("1.2.3.5"),
>>> ]

>>> # carnival_tasks.py
>>> import inventory as i
>>> class SetupFrontend(Task):
>>>    def run(self, **kwargs):
>>>        self.step(Frontend(), i.frontends)
"""

from typing import Any, Optional, Union
import warnings

from fabric.connection import Connection as SSHConnection  # type: ignore
from invoke.context import Context as LocalConnection  # type: ignore
from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy  # type: ignore


AnyConnection = Union[SSHConnection, LocalConnection]

"""
Список адресов которые трактуются как локальное соединение
.. deprecated:: 1.4
        Host is deprecated, use LocalHost or SSHHost explicitly
"""
LOCAL_ADDRS = [
    'local',
    'localhost',
]


class LocalHost:
    """
    Локальный хост, работает по локальному терминалу
    """

    def __init__(self, **context: Any) -> None:
        self.addr = "local"
        self.context = context

    def connect(self) -> LocalConnection:
        return LocalConnection()

    @property
    def host(self) -> str:
        """
        Remove user and port parts, return just address
        """

        h = self.addr

        if ':' in self.addr:
            h = h.split(":", maxsplit=1)[0]

        return h

    def __str__(self) -> str:
        return f"🖥 {self.host}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.host}>"


class SSHHost(LocalHost):
    """
    Удаленный хост, работает по SSH
    """

    def __init__(
        self,
        addr: str,
        ssh_user: Optional[str] = None, ssh_password: Optional[str] = None, ssh_port: int = 22,
        ssh_gateway: Optional['SSHHost'] = None,
        ssh_connect_timeout: int = 10,
        missing_host_key_policy: MissingHostKeyPolicy = AutoAddPolicy,

        **context: Any
     ):
        """
        :param addr: Адрес сервера
        :param ssh_user: Пользователь SSH
        :param ssh_password: Пароль SSH
        :param ssh_port: SSH порт
        :param ssh_connect_timeout: SSH таймаут соединения
        :param ssh_gateway: Gateway
        :param context: Контекст хоста
        """
        if "@" in addr:
            raise ValueError("Please set user in 'ssh_user' arg")

        self.addr = addr
        self.ssh_port = ssh_port
        self.context = context
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout
        self.ssh_gateway: Optional['SSHHost'] = ssh_gateway
        self.missing_host_key_policy = missing_host_key_policy

    def is_connection_local(self) -> bool:
        """
        Check if host's connection is local
        """
        warnings.warn(
            "is_connection_local is deprecated, use LocalHost or SSHHost explicitly",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.host.lower() in LOCAL_ADDRS

    def connect(self) -> SSHConnection:
        gateway = None
        if self.ssh_gateway:
            gateway = self.ssh_gateway.connect()
            assert isinstance(gateway, SSHConnection), f"{self.ssh_gateway} is not ssh connection"

        conn = SSHConnection(
            host=self.addr,
            port=self.ssh_port,
            user=self.ssh_user,
            connect_timeout=self.ssh_connect_timeout,
            gateway=gateway,
            connect_kwargs={
                'password': self.ssh_password,
            }
        )
        conn.client.set_missing_host_key_policy(self.missing_host_key_policy)
        return conn


AnyHost = Union[LocalHost, SSHHost]


class Host(SSHHost):
    """
    :param addr: Адрес сервера для SSH или "local" для локального соединения
    :param ssh_user: Пользователь SSH
    :param ssh_password: Пароль SSH
    :param ssh_port: SSH порт
    :param ssh_connect_timeout: SSH таймаут соединения
    :param ssh_gateway: Gateway
    :param context: Контекст хоста

    .. deprecated:: 1.4
        Host is deprecated, use LocalHost or SSHHost explicitly
    """
    def __init__(
        self,
        addr: str,
        ssh_user: Optional[str] = None, ssh_password: Optional[str] = None, ssh_port: int = 22,
        ssh_gateway: Optional['SSHHost'] = None, ssh_connect_timeout: int = 10,
        missing_host_key_policy: MissingHostKeyPolicy = AutoAddPolicy,
        **context: Any
    ):
        warnings.warn(
            "Host is deprecated, use LocalHost or SSHHost explicitly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(
            addr,
            ssh_user=ssh_user, ssh_password=ssh_password, ssh_port=ssh_port,
            ssh_gateway=ssh_gateway, ssh_connect_timeout=ssh_connect_timeout,
            missing_host_key_policy=missing_host_key_policy, **context
        )

    def connect(self) -> AnyConnection:
        if self.addr in LOCAL_ADDRS:
            return LocalConnection()

        return super().connect()
