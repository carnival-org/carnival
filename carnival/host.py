"""
Объект, представляющий единицу оборудования.

Carnival не предоставляет никаких сложных абстракций для работы с группами хостов,
подразумевая что вы будете использовать встроенные коллекции python и организуете
работу так, как будет удобно для вашей задачи.
В простом случае, можно передавать хосты прямо в коде файла `carnival_tasks.py`.
В более сложных, создать списки в отдельном файле, например `inventory.py`
"""

import typing

from fabric.connection import Connection as SSHConnection  # type: ignore
from invoke.context import Context as LocalConnection  # type: ignore
from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy


AnyConnection = typing.Union[SSHConnection, LocalConnection]


class LocalHost:
    """
    Локальный хост, работает по локальному терминалу

    :param context: Контекст хоста
    """

    def __init__(self, **context: typing.Any) -> None:
        self.addr = "local"
        self.context = context
        self.context['host'] = self

    def connect(self) -> LocalConnection:
        return LocalConnection()

    def __str__(self) -> str:
        return f"🖥 {self.addr}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.addr}>"


class SSHHost(LocalHost):
    """
    Удаленный хост, работает по SSH
    """

    def __init__(
        self,
        addr: str,
        ssh_user: typing.Optional[str] = None, ssh_password: typing.Optional[str] = None, ssh_port: int = 22,
        ssh_gateway: typing.Optional['SSHHost'] = None,
        ssh_connect_timeout: int = 10,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,

        **context: typing.Any
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
        if ":" in addr:
            raise ValueError("Please set port in 'ssh_port' arg")

        if "@" in addr:
            raise ValueError("Please set user in 'ssh_user' arg")

        super().__init__(**context)

        self.addr = addr
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout
        self.ssh_gateway: typing.Optional['SSHHost'] = ssh_gateway
        self.missing_host_key_policy = missing_host_key_policy

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


AnyHost = typing.Union[LocalHost, SSHHost]
