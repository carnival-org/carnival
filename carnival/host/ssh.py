from types import TracebackType
import typing
from threading import Thread
import sys

from paramiko.channel import ChannelStdinFile, ChannelFile, ChannelStderrFile
from paramiko.client import MissingHostKeyPolicy, AutoAddPolicy, SSHClient
from paramiko.config import SSH_PORT

from carnival.host import results
from carnival.host import _base


class ResultPromise(results.ResultPromise):
    def __init__(
        self,
        stdin: ChannelStdinFile,
        stdout: ChannelFile,
        stderr: ChannelStderrFile,
        hide: bool,
    ) -> None:
        self.stdin: ChannelStdinFile = stdin
        self.stdout: ChannelFile = stdout
        self.stderr: ChannelStderrFile = stderr

        self.threads: typing.List[Thread] = []

        if not hide:
            self._track_output()

    def is_done(self) -> bool:
        return self.stdout.channel.exit_status_ready()

    def wait(self) -> results.Result:
        for t in self.threads:
            t.join()

        retcode = self.stdout.channel.recv_exit_status()
        return results.Result(
            returncode=retcode,
            stdout=self.stdout,
            stderr=self.stderr,
            stdin=self.stdin,
        )

    def _track_output(self) -> None:
        def output_thread(fromio: results._IOFileLike, toio: results._IOFileLike) -> None:
            while not self.is_done():
                toio.write(fromio.read(self.bufsize).decode())
            toio.write(fromio.read(-1).decode())

        self.threads.append(Thread(target=output_thread, kwargs={"fromio": self.stdout, "toio": sys.stdout}))
        self.threads.append(Thread(target=output_thread, kwargs={"fromio": self.stderr, "toio": sys.stderr}))

        for t in self.threads:
            t.start()


class SSHConnection(_base.ConnectionBase):
    def __init__(
        self,
        conn: SSHClient,
        gw_conn: typing.Optional["SSHConnection"] = None,
        run_timeout: int = 60
    ):
        self.conn = conn
        self.gw_conn = gw_conn
        self.run_timeout = run_timeout

    def close(self) -> None:
        self.conn.close()

    def run(self, command: str, hide: bool) -> ResultPromise:
        """
        Выполнить команду

        :param command: команда
        :param hide: скрыть вывод
        """
        assert self.conn is not None
        stdin, stdout, stderr = self.conn.exec_command(command, timeout=self.run_timeout, get_pty=True)
        return ResultPromise(stdin=stdin, stdout=stdout, stderr=stderr, hide=hide)

    def __enter__(self) -> "SSHConnection":
        return self

    def __exit__(self, exc_type: typing.Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        self.close()
        if self.gw_conn is not None:
            self.gw_conn.close()


class SSHHost(_base.HostBase):
    def __init__(
        self,
        host: str,
        port: int = SSH_PORT,
        ssh_user: typing.Optional[str] = None, ssh_password: typing.Optional[str] = None,
        ssh_gateway: typing.Optional['SSHHost'] = None,
        ssh_connect_timeout: int = 10,
        missing_host_key_policy: typing.Type[MissingHostKeyPolicy] = AutoAddPolicy,
     ):
        """
        Хост с доступом по SSH

        :param host: адрес без порта и имени пользователя
        :param port: ssh порт
        :param ssh_user: имя пользователя
        :param ssh_password: пароль
        :param ssh_gateway: proxyjump
        :param ssh_connect_timeout: таймаут соединения
        :param missing_host_key_policy: политика при отсутствии ключа сервера
        """
        if "@" in host:
            raise ValueError("Please set user in 'ssh_user' arg")

        if ":" in host:
            raise ValueError("Please set port in 'port' arg")

        self.host = host
        self.port = port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_timeout = ssh_connect_timeout
        self.ssh_gateway: typing.Optional['SSHHost'] = ssh_gateway
        self.missing_host_key_policy = missing_host_key_policy

    def connect(self) -> SSHConnection:
        """
        :returns: Возвращает контекстменеджер соединения для хоста
        """
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(self.missing_host_key_policy)

        gw_conn: typing.Optional[SSHConnection] = None
        sock = None
        if self.ssh_gateway:
            gw_conn = self.ssh_gateway.connect()
            transport = gw_conn.conn.get_transport()
            assert transport is not None
            sock = transport.open_channel(
                'direct-tcpip', (self.host, self.port), ('', 0)
            )

        client.connect(
            hostname=self.host,
            port=self.port,
            username=self.ssh_user,
            password=self.ssh_password,
            timeout=self.ssh_connect_timeout,
            sock=sock,  # type: ignore
        )

        return SSHConnection(conn=client, gw_conn=gw_conn)

    def get_address(self) -> str:
        return self.host

    def get_ssh_addess(self) -> str:
        """
        Return `user@addr` if user given, else `addr`
        """

        if self.ssh_user:
            return f"{self.ssh_user}@{self.get_address()}"
        return self.get_address()


__all__ = [
    'SSHConnection',
    'SSHHost',
]
