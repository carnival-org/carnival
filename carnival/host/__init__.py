import abc
import typing
from contextlib import contextmanager
import copy

from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy
from fabric.connection import Connection as FabricConnection  # type: ignore

from carnival.host.connection import Connection
from carnival.host import _ssh_connection
from carnival.host import _local_connection

HostContextT = typing.TypeVar("HostContextT")
NewHostContextT = typing.TypeVar("NewHostContextT")


class Host(typing.Generic[HostContextT], metaclass=abc.ABCMeta):
    def __init__(self, context: HostContextT) -> None:
        self.addr = ""
        self.context = context

    @abc.abstractmethod
    def connect(self) -> typing.ContextManager[Connection]: ...

    def __str__(self) -> str:
        return f"🖥 {self.addr}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.addr}>"


class LocalHost(Host[HostContextT]):
    """
    Локальный хост, работает по локальному терминалу
    """

    def __init__(self, context: HostContextT) -> None:
        self.addr: str = "localhost"
        super().__init__(context)

    def with_context(self, context: NewHostContextT) -> "LocalHost[NewHostContextT]":  # TODO: Self type
        new_host = typing.cast(LocalHost[NewHostContextT], copy.deepcopy(self))
        new_host.context = context
        return new_host

    @contextmanager
    def connect(self) -> typing.Generator[_local_connection._LocalConnection, None, None]:
        yield _local_connection._LocalConnection()


class SshHost(Host[HostContextT]):
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
    def connect(self) -> typing.Generator[_ssh_connection._SSHConnection, None, None]:
        gateway = None
        if self.ssh_gateway:
            gateway = self.ssh_gateway.connect()

        conn = FabricConnection(
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
        yield _ssh_connection._SSHConnection(conn)
        conn.close()


localhost = LocalHost[None](None)


__all__ = (
    'Host',
    'LocalHost',
    'localhost',
    'SshHost',
)
