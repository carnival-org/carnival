import typing

from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy
from paramiko.config import SSH_PORT

from carnival.hosts.base.host import Host
from .connection import SshConnection
from .ssh_config import SSHConfig


class SshHost(Host):
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
        port: int = SSH_PORT,
        use_sudo: bool = False,

        user: typing.Optional[str] = None,
        password: typing.Optional[str] = None,

        gateway: typing.Optional['SshHost'] = None,
        connect_timeout: int = 10,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,
    ):
        """
        :param addr: Адрес сервера
        :param port: SSH порт
        :param user: Пользователь SSH
        :param password: Пароль SSH
        :param gateway: Gateway
        :param connect_timeout: SSH таймаут соединения
        :param missing_host_key_policy: политика system host keys
        """
        super(SshHost, self).__init__(use_sudo=use_sudo)

        if ":" in addr:
            raise ValueError("Please set port in 'ssh_port' arg")
        if "@" in addr:
            raise ValueError("Please set user in 'ssh_user' arg")

        self.addr = addr
        self.ssh_config = SSHConfig()
        self.connect_config = self.ssh_config.lookup(hostname=addr, missing_host_key_policy=missing_host_key_policy)
        self.connect_config.port = port

        self.connect_config.user = user or self.connect_config.user
        self.connect_config.password = password or self.connect_config.password
        self.connect_config.connecttimeout = connect_timeout or self.connect_config.connecttimeout

        if gateway:
            self.connect_config.proxycommand = gateway.get_proxy_command()

    def get_proxy_command(self) -> str:
        # ssh -W %h:%p jumphost.nixcraft.com
        addr = f"{self.addr}:{self.connect_config.port}"
        if self.connect_config.user:
            addr = f"{self.connect_config.user}@{addr}"

        return f"ssh -W %h:%p {addr}"

    def connect(self) -> SshConnection:
        """
        :returns: Возвращает контекстменеджер соединения для хоста
        """
        return SshConnection(
            host=self,
            conf=self.connect_config,
            use_sudo=self.use_sudo,
        )
