"""
Объект, представляющий единицу оборудования.

Carnival не предоставляет никаких сложных абстракций для работы с группами хостов,
подразумевая что вы будете использовать встроенные коллекции python и организуете
работу так, как будет удобно для вашей задачи.
В простом случае, можно передавать хосты прямо в коде файла `carnival_tasks.py`.
В более сложных, создать списки в отдельном файле, например `inventory.py`.

>>> @dataclass
>>> class SiteContext:
>>>     port: int = 80
>>>     site_directory: str = "/var/www"
>>>
>>> site1 = SSHHost("1.2.3.4", context=SiteContext(port=443, site_directory="/opt/www"))
>>> site2 = SSHHost("1.2.3.5", context=SiteContext(port=443))
>>> site3 = LocalHost(context=SiteContext(site_directory="/home/a1fred/www"))
"""

import abc
import typing
import copy
from contextlib import contextmanager

from carnival.connection import LocalConnection, SSHConnection, AnyConnection
from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy


HostContextT = typing.TypeVar("HostContextT")
NewHostContextT = typing.TypeVar("NewHostContextT")


class AnyHost(typing.Generic[HostContextT], metaclass=abc.ABCMeta):
    context: HostContextT
    addr: str

    @abc.abstractmethod
    def connect(self) -> typing.ContextManager[AnyConnection]: ...

    def __str__(self) -> str:
        return f"🖥 {self.addr}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.addr}>"


class LocalHost(AnyHost[HostContextT]):
    """
    Локальный хост, работает по локальному терминалу
    """

    def __init__(self, context: HostContextT) -> None:
        self.context = context
        self.addr: str = "localhost"

    def with_context(self, context: NewHostContextT) -> "LocalHost[NewHostContextT]":  # TODO: Self type
        new_host = typing.cast(LocalHost[NewHostContextT], copy.deepcopy(self))
        new_host.context = context
        return new_host

    @contextmanager
    def connect(self) -> typing.Generator[LocalConnection, None, None]:
        yield LocalConnection()


class SshHost(AnyHost[HostContextT]):
    """
    Удаленный хост, работает по SSH
    """

    def __init__(
        self,
        addr: str,
        context: HostContextT,

        ssh_user: typing.Optional[str] = None, ssh_password: typing.Optional[str] = None,
        ssh_port: int = 22,
        ssh_gateway: typing.Optional['SshHost[typing.Any]'] = None,
        ssh_connect_timeout: int = 10,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,
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

        self.context = context
        self.addr = addr
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout
        self.ssh_gateway = ssh_gateway
        self.missing_host_key_policy = missing_host_key_policy

    @contextmanager
    def connect(self) -> typing.Generator[SSHConnection, None, None]:
        from fabric.connection import Connection  # type: ignore
        gateway = None
        if self.ssh_gateway:
            gateway = self.ssh_gateway.connect()
            assert isinstance(gateway, SSHConnection), f"{self.ssh_gateway} is not ssh connection"

        conn = Connection(
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
        yield SSHConnection(conn)
        conn.close()


localhost = LocalHost[None](None)


__all__ = (
    'localhost',
    'SshHost',
)
