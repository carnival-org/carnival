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
    def __init__(self, context: HostContextT, sudo: bool = False) -> None:
        self.addr = ""
        self.context = context
        self.sudo = sudo

    def with_context(self, context: NewHostContextT) -> "Host[NewHostContextT]":  # TODO: Self type
        new_host = typing.cast(Host[NewHostContextT], copy.deepcopy(self))
        new_host.context = context
        return new_host

    def __str__(self) -> str:
        return f"🖥 {self.addr}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.addr}>"

    @abc.abstractmethod
    def connect(self) -> typing.ContextManager[Connection]: ...


class _LocalHost(Host[HostContextT]):
    """
    Локальный хост, работает по локальному терминалу
    """

    def __init__(self, context: HostContextT, sudo: bool = False) -> None:
        self.addr: str = "localhost"
        super().__init__(context=context, sudo=sudo)

    @contextmanager
    def connect(self) -> typing.Generator[_local_connection.LocalConnection, None, None]:
        yield _local_connection.LocalConnection(sudo=self.sudo)


def LocalHost(context: HostContextT, sudo: bool = False) -> Host[HostContextT]:
    return _LocalHost(context=context, sudo=sudo)


class _SshHost(Host[HostContextT]):
    """
    Удаленный хост, работает по SSH
    """

    def __init__(
        self,
        addr: str,
        context: HostContextT,

        ssh_user: typing.Optional[str] = None, ssh_password: typing.Optional[str] = None,
        ssh_port: int = 22,
        ssh_gateway: typing.Optional['_SshHost[typing.Any]'] = None,
        ssh_connect_timeout: int = 10,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,

        sudo: bool = False,
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

        super().__init__(context=context, sudo=sudo)

        self.addr = addr
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout
        self.ssh_gateway = ssh_gateway
        self.missing_host_key_policy = missing_host_key_policy

    @contextmanager
    def connect(self) -> typing.Generator[_ssh_connection.SSHConnection, None, None]:
        gateway = None
        if self.ssh_gateway:
            gateway = self.ssh_gateway.connect().__enter__().c

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
        conn.open()
        yield _ssh_connection.SSHConnection(conn, sudo=self.sudo)
        conn.close()


def SshHost(
    addr: str,
    context: HostContextT,

    ssh_user: typing.Optional[str] = None, ssh_password: typing.Optional[str] = None,
    ssh_port: int = 22,
    ssh_gateway: typing.Optional['_SshHost[typing.Any]'] = None,
    ssh_connect_timeout: int = 10,
    missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,

    sudo: bool = False,
) -> Host[HostContextT]:
    return _SshHost(
        addr=addr,
        context=context,

        ssh_user=ssh_user, ssh_password=ssh_password,
        ssh_port=ssh_port,
        ssh_gateway=ssh_gateway,
        ssh_connect_timeout=ssh_connect_timeout,
        missing_host_key_policy=missing_host_key_policy,

        sudo=sudo,
    )


localhost = LocalHost(None)
localhost_connection = localhost.connect().__enter__()

__all__ = (
    'Host',
    'LocalHost',
    'localhost',
    'localhost_connection',
    'SshHost',
)
