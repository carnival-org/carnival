import os.path
import typing

from paramiko.client import MissingHostKeyPolicy, SSHClient, RejectPolicy
from paramiko.config import SSH_PORT, SSHConfig as ParamikoSshConfig, SSHConfigDict
from paramiko.proxy import ProxyCommand


class HostnameConfig:
    # https://man.openbsd.org/ssh_config

    def __init__(
        self,
        hostname: str,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy],
        conf: SSHConfigDict,
    ):
        if 'proxyjump' in conf:
            # TODO: implement proxyjumps?
            raise ValueError("'proxyjump' is not supported for now ;(")

        self.missing_host_key_policy = missing_host_key_policy
        self.hostname: str = hostname
        self.port: int = SSH_PORT
        self.user: typing.Optional[str] = None
        self.password: typing.Optional[str] = None
        self.key_filename: typing.Optional[str] = None
        self.compression = False
        self.proxycommand: typing.Optional[str] = None
        self.connecttimeout: typing.Optional[int] = None

        if 'hostname' in conf:
            self.hostname = conf.get('hostname') or self.hostname

        if 'stricthostkeychecking' in conf:
            if conf.as_bool('stricthostkeychecking') is True:
                self.missing_host_key_policy = RejectPolicy
            else:
                self.missing_host_key_policy = MissingHostKeyPolicy

        if 'port' in conf:
            self.port = conf.as_int('port')

        if 'user' in conf:
            self.user = conf.get('user')

        if 'identityfile' in conf:
            self.key_filename = conf.get('identityfile')

        if 'compression' in conf:
            self.compression = conf.as_bool("compression")

        if 'proxycommand' in conf:
            self.proxycommand = conf.get('proxycommand')

        if 'connecttimeout' in conf:
            self.connecttimeout = conf.as_int('connecttimeout')

    def connect(self) -> SSHClient:
        conn = SSHClient()
        conn.load_system_host_keys()
        conn.set_missing_host_key_policy(self.missing_host_key_policy)

        sock = None
        if self.proxycommand is not None:
            sock = ProxyCommand(self.proxycommand)

        conn.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.user,
            password=self.password,
            look_for_keys=True,
            key_filename=self.key_filename,
            compress=self.compression,
            auth_timeout=10,
            timeout=self.connecttimeout,
            sock=sock,  # type: ignore
        )

        return conn


class SSHConfig:
    default_ssh_config_chain = ("/etc/ssh/ssh_config", "~/.ssh/config")

    def __init__(self, config_path: typing.Optional[str] = None):
        self.config = ParamikoSshConfig()

        chain = list(self.default_ssh_config_chain)
        if config_path:
            chain.append(config_path)

        for config_path in chain:
            path = os.path.expanduser(config_path)
            if os.path.exists(path):
                with open(path, 'r') as fp:
                    self.config.parse(fp)
            else:
                print(f"[WARN] ssh config at {path} not exist!")

    def lookup(self, hostname: str, missing_host_key_policy: typing.Type[MissingHostKeyPolicy],) -> HostnameConfig:
        return HostnameConfig(
            hostname,
            missing_host_key_policy=missing_host_key_policy,
            conf=self.config.lookup(hostname),
        )
