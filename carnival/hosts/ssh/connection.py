import typing
from contextlib import contextmanager

from paramiko.client import SSHClient

from carnival.hosts.base.connection import Connection
from carnival.hosts.base.result_promise import ResultPromise
from carnival.hosts.base.stat_result import StatResult

from .result_promise import SshResultPromise
from .ssh_config import HostnameConfig


if typing.TYPE_CHECKING:
    from carnival.hosts.ssh import SshHost


class SshConnection(Connection):
    def __init__(
        self,
        host: "SshHost",
        conf: HostnameConfig,
        use_sudo: bool = False,
    ) -> None:
        super().__init__(host=host, use_sudo=use_sudo)
        self.host: "SshHost" = host
        self.conf = conf
        self.conn: typing.Optional[SSHClient] = None

    def __enter__(self) -> "SshConnection":
        # Connection now lazy, see `._ensure_connection`
        # self.conn = self.conf.connect()
        return self

    def __exit__(self, *args: typing.Any) -> None:
        if self.conn is not None:
            self.conn.close()

    def _ensure_connection(self) -> None:
        if self.conn is None:
            self.conn = self.conf.connect()

    def run_promise(
        self,
        command: str,
        use_sudo: bool,
        env: typing.Optional[typing.Dict[str, str]] = None,
        cwd: typing.Optional[str] = None,
        timeout: int = 60,
    ) -> ResultPromise:
        self._ensure_connection()
        assert self.conn is not None, "Connection is not opened"
        return SshResultPromise(
            conn=self.conn,
            command=command,
            env=env,
            cwd=cwd,
            use_sudo=use_sudo,
            timeout=timeout,
        )

    def file_stat(self, path: str) -> StatResult:
        self._ensure_connection()
        assert self.conn is not None, "Connection is not opened"
        sftp = self.conn.open_sftp()

        stat = sftp.stat(path)
        assert stat.st_mode is not None
        assert stat.st_size is not None
        assert stat.st_uid is not None
        assert stat.st_gid is not None
        assert stat.st_atime is not None

        return StatResult(
            st_mode=stat.st_mode,
            st_size=stat.st_size,
            st_uid=stat.st_uid,
            st_gid=stat.st_gid,
            st_atime=stat.st_atime,
        )

    @contextmanager
    def file_read(self, path: str) -> typing.Generator[typing.IO[bytes], None, None]:
        self._ensure_connection()
        assert self.conn is not None, "Connection is not opened"
        sftp = self.conn.open_sftp()
        with sftp.open(path, 'rb') as reader:
            typed_reader = typing.cast(typing.IO[bytes], reader)
            yield typed_reader

    @contextmanager
    def file_write(self, path: str) -> typing.Generator[typing.IO[bytes], None, None]:
        self._ensure_connection()
        assert self.conn is not None, "Connection is not opened"
        sftp = self.conn.open_sftp()
        with sftp.open(path, 'wb') as writer:
            typed_writer = typing.cast(typing.IO[bytes], writer)
            yield typed_writer
