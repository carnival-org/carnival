import typing
from contextlib import contextmanager

from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy, SSHClient
from paramiko.config import SSH_PORT

from carnival.hosts import base


class SshConnection(base.Connection):
    def __init__(
        self,
        host: "SshHost",
        ssh_addr: str,
        ssh_port: int = SSH_PORT,
        ssh_user: typing.Optional[str] = None,
        ssh_password: typing.Optional[str] = None,
        ssh_gateway: typing.Optional["SshHost"] = None,
        ssh_connect_timeout: int = 10,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,
        run_timeout: int = 120,
    ) -> None:
        super().__init__(host, run_timeout=run_timeout)
        self.host: "SshHost" = host

        self.ssh_gateway = ssh_gateway
        self.ssh_addr = ssh_addr
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout

        self.gw_conn: typing.Optional[SshConnection] = None
        self.conn = SSHClient()
        self.conn.load_system_host_keys()
        self.conn.set_missing_host_key_policy(missing_host_key_policy)

    def __enter__(self) -> "SshConnection":
        sock = None
        if self.ssh_gateway:
            self.gw_conn = self.ssh_gateway.connect()
            transport = self.gw_conn.conn.get_transport()
            assert transport is not None
            sock = transport.open_channel('direct-tcpip', (self.ssh_addr, self.ssh_port), ('', 0))

        self.conn.connect(
            hostname=self.ssh_addr,
            port=self.ssh_port,
            username=self.ssh_user,
            password=self.ssh_password,
            timeout=self.ssh_connect_timeout,
            sock=sock,  # type: ignore
        )
        return self

    def __exit__(self, *args: typing.Any) -> None:
        self.conn.close()
        if self.gw_conn is not None:
            self.gw_conn.conn.close()

    def run(
        self,
        command: str,
        hide: bool = False, warn: bool = False, cwd: typing.Optional[str] = None,
    ) -> base.Result:
        assert self.conn is not None
        initial_command = command

        if cwd is not None:
            command = f"cd {cwd}; {command}"

        stdin, stdout, stderr = self.conn.exec_command(
            command,
            timeout=self.run_timeout,
            get_pty=False,  # Combines stdout and stderr, we dont want it
        )
        retcode = stdout.channel.recv_exit_status()

        stdout_str = stdout.read().decode().replace("\r", "")
        stderr_str = stderr.read().decode().replace("\r", "")
        stdout.close()
        stderr.close()
        stdin.close()

        return base.Result(
            return_code=retcode,
            stdout=stdout_str,
            stderr=stderr_str,

            command=initial_command,
            hide=hide,
            warn=warn,
        )

    def file_stat(self, path: str) -> base.StatResult:
        sftp = self.conn.open_sftp()

        stat = sftp.stat(path)
        assert stat.st_mode is not None
        assert stat.st_size is not None
        assert stat.st_uid is not None
        assert stat.st_gid is not None
        assert stat.st_atime is not None

        return base.StatResult(
            st_mode=stat.st_mode,
            st_size=stat.st_size,
            st_uid=stat.st_uid,
            st_gid=stat.st_gid,
            st_atime=stat.st_atime,
        )

    @contextmanager
    def file_read(self, path: str) -> typing.Generator[typing.IO[bytes], None, None]:
        sftp = self.conn.open_sftp()
        with sftp.open(path, 'rb') as reader:
            typed_reader = typing.cast(typing.IO[bytes], reader)
            yield typed_reader

    @contextmanager
    def file_write(self, path: str) -> typing.Generator[typing.IO[bytes], None, None]:
        with self as conn:
            sftp = conn.conn.open_sftp()
            with sftp.open(path, 'wb') as writer:
                typed_writer = typing.cast(typing.IO[bytes], writer)
                yield typed_writer


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

        ssh_user: typing.Optional[str] = None,
        ssh_password: typing.Optional[str] = None,
        ssh_port: int = 22,
        ssh_gateway: typing.Optional['SshHost'] = None,
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
        """
        if ":" in addr:
            raise ValueError("Please set port in 'ssh_port' arg")
        if "@" in addr:
            raise ValueError("Please set user in 'ssh_user' arg")

        super().__init__()

        self.addr = addr
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout
        self.ssh_gateway = ssh_gateway
        self.missing_host_key_policy = missing_host_key_policy

    def connect(self) -> SshConnection:
        """
        :returns: Возвращает контекстменеджер соединения для хоста
        """
        return SshConnection(
            host=self,
            ssh_addr=self.addr,
            ssh_port=self.ssh_port,
            ssh_user=self.ssh_user,
            ssh_password=self.ssh_password,
            ssh_gateway=self.ssh_gateway,
            ssh_connect_timeout=self.ssh_connect_timeout,
            missing_host_key_policy=self.missing_host_key_policy,
        )
