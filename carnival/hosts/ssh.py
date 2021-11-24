import typing

from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy
from fabric.connection import Connection as FabricConnection  # type: ignore

from carnival.hosts import base


class SshConnection(base.Connection):
    def __init__(
        self,
        host: "SshHost",
    ) -> None:
        self.host: "SshHost" = host

        self._c: typing.Optional[FabricConnection] = None
        self._gateway: typing.Optional[FabricConnection] = None

    def __enter__(self) -> "SshConnection":
        if self.host.ssh_gateway is not None:
            self._gateway = self.host.ssh_gateway.connect().__enter__()._c

        self._c = FabricConnection(
            host=self.host.addr,
            port=self.host.ssh_port,
            user=self.host.ssh_user,
            connect_timeout=self.host.ssh_connect_timeout,
            gateway=self._gateway,
            connect_kwargs={
                'password': self.host.ssh_password,
            }
        )
        self._c.client.set_missing_host_key_policy(self.host.missing_host_key_policy)
        return self

    def __exit__(self, *args: typing.Any) -> None:
        assert self._c is not None
        self._c.close()

        if self._gateway is not None:
            self._gateway.close()

    def run(
        self,
        command: str,
        hide: bool = False, warn: bool = True, cwd: typing.Optional[str] = None,
    ) -> base.Result:
        assert self._c is not None, "Connection is not created"
        # lazy connect
        if self._c.is_connected is False:
            self._c.open()

        handler_kwargs = {
            "command": command,
            "hide": hide,
            "pty": True,
            "warn": warn,
        }

        handler = self._c.run

        if cwd is not None:
            with self._c.cd(cwd):
                return base.Result.from_invoke_result(handler(**handler_kwargs))

        return base.Result.from_invoke_result(handler(**handler_kwargs))


class SshHost(base.Host):
    """
    SSH хост
    """

    addr: str
    """
    Домен либо ip хоста
    """

    def __init__(
        self,
        addr: str,

        ssh_user: typing.Optional[str] = None, ssh_password: typing.Optional[str] = None,
        ssh_port: int = 22,
        ssh_gateway: typing.Optional['SshHost'] = None,
        ssh_connect_timeout: int = 10,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,

        **context: typing.Any,
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
        self.ssh_gateway = ssh_gateway
        self.missing_host_key_policy = missing_host_key_policy

    def connect(self) -> SshConnection:
        return SshConnection(host=self)
