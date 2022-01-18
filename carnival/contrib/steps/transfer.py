import os.path
import typing
from io import BytesIO
from hashlib import sha1
from uuid import uuid4

from tqdm import tqdm  # type: ignore
from paramiko.config import SSH_PORT

from carnival import Connection, localhost_connection, SshHost
from carnival.templates import render
from carnival.steps import shortcuts, Step, validators


def _file_sha1sum(c: Connection, fpath: str) -> typing.Optional[str]:
    if not shortcuts.is_file(c, fpath):
        return None
    return c.run(f"cat {fpath} | shasum -a1", hide=True).stdout.strip(" -\t\n")


def _transfer_file(
    reader: typing.IO[bytes],
    writer_conn: Connection,
    writer_dst_path: str,
    dst_file_size: int,
    dst_file_path: str,
    bufsize: int = 32768,
) -> None:
    write_size = 0

    # Create dirs if needed
    dirname = os.path.dirname(writer_dst_path)
    if dirname:
        writer_conn.run(f"mkdir -p {dirname}", hide=True)

    tempfile_path = os.path.join(writer_conn.tempdir, f'carnival.{uuid4()}.tmp')

    with tqdm(
        desc=f"Transferring {dst_file_path}",
            unit='B', unit_scale=True, total=dst_file_size,
            leave=False,
    ) as pbar:
        with writer_conn.file_write(tempfile_path) as writer:
            while True:
                data = reader.read(bufsize)
                if len(data) == 0:
                    break

                writer.write(data)
                pbar.update(len(data))
                write_size += len(data)

    if dst_file_size != write_size:
        writer_conn.run(f"rm {tempfile_path}")
        raise IOError(f"size mismatch! {dst_file_size} != {write_size}")

    writer_conn.run(f"mv {tempfile_path} {writer_dst_path}")
    # если используется sudo - нужно назначить владельца
    user_id = shortcuts.get_user_id(writer_conn)
    user_group_id = shortcuts.get_user_group_id(writer_conn)
    writer_conn.run(f"chown {user_id}:{user_group_id} {writer_dst_path}")

    Step.log_action(writer_dst_path, "transferred")


class GetFile(Step):
    """
    Скачать файл с удаленного сервера на локальный диск
    """
    def __init__(self, remote_path: str, local_path: str):
        """
        :param remote_path: Путь до файла на сервере
        :param local_path: Локальный путь назначения
        """
        self.remote_path = remote_path
        self.local_path = local_path

    def get_name(self) -> str:
        return f"{super().get_name()}(remote_path={self.remote_path}, local_path={self.local_path})"

    def get_validators(self) -> typing.List["validators.StepValidatorBase"]:
        return [
            validators.IsFileValidator(self.remote_path),
            validators.Not(
                validators.Local(validators.IsDirectoryValidator(self.local_path)),
                error_message=f"{self.remote_path} must be full file path, not directory",
            )
        ]

    def run(self, c: "Connection") -> None:
        remote_sha1 = _file_sha1sum(c, self.remote_path)
        local_sha1 = _file_sha1sum(localhost_connection, self.local_path)
        if remote_sha1 is not None and local_sha1 is not None:
            if remote_sha1 == local_sha1:
                return

        with c.file_read(self.remote_path) as reader:
            dst_file_size = c.file_stat(self.remote_path).st_size
            _transfer_file(
                reader=reader,
                writer_conn=localhost_connection,
                writer_dst_path=self.local_path,
                dst_file_size=dst_file_size, dst_file_path=self.remote_path,
            )


class PutFile(Step):
    """
    Закачать файл на сервер

    """
    def __init__(self, local_path: str, remote_path: str, chmod: typing.Optional[str] = None):
        """
        :param local_path: путь до локального файла
        :param remote_path: путь куда сохранить на сервере
        """
        self.local_path = local_path
        self.remote_path = remote_path
        self.chmod = chmod

    def get_name(self) -> str:
        return f"{super().get_name()}(local_path={self.local_path}, remote_path={self.remote_path})"

    def get_validators(self) -> typing.List["validators.StepValidatorBase"]:
        return [
            validators.Local(validators.IsFileValidator(self.local_path)),
            validators.Not(
                validators.IsDirectoryValidator(self.remote_path),
                error_message=f"{self.remote_path} must be full file path, not directory",
            ),
        ]

    def run(self, c: "Connection") -> None:
        remote_sha1 = _file_sha1sum(c, self.remote_path)
        local_sha1 = _file_sha1sum(localhost_connection, self.local_path)
        if remote_sha1 is not None and local_sha1 is not None:
            if remote_sha1 == local_sha1:
                return

        with localhost_connection.file_read(self.local_path) as reader:
            dst_file_size = localhost_connection.file_stat(self.local_path).st_size
            _transfer_file(
                reader=reader,
                writer_conn=c,
                writer_dst_path=self.remote_path,
                dst_file_size=dst_file_size, dst_file_path=self.remote_path,
            )
        if self.chmod is not None:
            c.run(f"chmod {self.chmod} {self.remote_path}")
            self.log_action(self.remote_path, f"chmod set to {self.chmod}")


class PutTemplate(Step):
    """
    Отрендерить файл с помощью jinja-шаблонов и закачать на сервер
    См раздел templates.
    """

    def __init__(self, template_path: str, remote_path: str, context: typing.Dict[str, typing.Any]):
        """
        :param template_path: путь до локального файла jinja
        :param remote_path: путь куда сохранить на сервере
        :param context: контекс для рендеринга jinja2
        """
        self.template_path = template_path
        self.remote_path = remote_path
        self.context = context

    def get_name(self) -> str:
        return f"{super().get_name()}(template_path={self.template_path})"

    def get_validators(self) -> typing.List["validators.StepValidatorBase"]:
        return [
            validators.TemplateValidator(self.template_path, context=self.context),
        ]

    def run(self, c: "Connection") -> None:
        filebytes = render(template_path=self.template_path, **self.context).encode()

        remote_sha1 = _file_sha1sum(c, self.remote_path)
        local_sha1 = sha1(filebytes).hexdigest()

        if remote_sha1 is not None and local_sha1 is not None:
            if remote_sha1 == local_sha1:
                return

        _transfer_file(
            reader=BytesIO(filebytes),
            writer_conn=c,
            writer_dst_path=self.remote_path,
            dst_file_size=len(filebytes), dst_file_path=self.remote_path,
        )


class Rsync(Step):
    """
    Залить папку с локального диска на сервер по rsync
    """

    def __init__(
        self,
        src_dir_or_file: str,
        dst_dir: str,

        rsync_opts: typing.Optional[str] = None,
        ssh_opts: str = '',
        rsync_command: str = "rsync",
        rsync_timeout: int = 120,
    ):
        """
        :param src_dir_or_file: локальный путь до папки или файла
        :param dst_dir: путь куда нужно залить
        :param rsync_opts: параметры команды rsync
        :param ssh_opts: параметры ssh
        :param rsync_command: путь до rsync
        """
        self.src_dir_or_file = src_dir_or_file
        self.dst_dir = dst_dir
        self.rsync_opts = rsync_opts or "--progress -pthrvz --timeout=60"
        self.ssh_opts = ssh_opts
        self.rsync_command = rsync_command
        self.rsync_timeout = rsync_timeout

    def get_name(self) -> str:
        return f"{super().get_name()}(source={self.src_dir_or_file}, dest={self.dst_dir})"

    @staticmethod
    def _host_for_ssh(host: SshHost) -> str:
        """
        Return `user@addr` if user given, else `addr`
        """

        if host.connect_config.user:
            return f"{host.connect_config.user}@{host.addr}"
        return host.addr

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.InlineValidator(
                lambda c: not isinstance(c.host, SshHost),
                "remote host must be ssh connected host",
            ),
            validators.Local(validators.CommandRequiredValidator("rsync")),
            validators.Or(
                validators=[
                    validators.Local(validators.IsFileValidator(self.src_dir_or_file)),
                    validators.Local(validators.IsDirectoryValidator(self.src_dir_or_file)),
                ],
                error_message="'src_dir_or_file' must be file or directory",
            )
        ]

    def run(self, c: "Connection") -> typing.Any:
        assert isinstance(c.host, SshHost)

        # Create dirs if needed
        dirname = os.path.dirname(self.dst_dir)
        if dirname:
            c.run(f"mkdir -p {dirname}", hide=True)

        ssh_opts = self.ssh_opts
        if c.host.connect_config.port != SSH_PORT:
            ssh_opts = f"-p {c.host.connect_config.port} {ssh_opts}"
        if c.host.connect_config.proxycommand is not None:
            ssh_opts = f"-o ProxyCommand='{c.host.connect_config.proxycommand}'"
        ssh_opts = ssh_opts.strip()
        if ssh_opts:
            ssh_opts = f'-e "ssh {ssh_opts.strip()}"'

        rsync_opts = self.rsync_opts
        if c.use_sudo is True:
            rsync_opts = f'--rsync-path="sudo -n rsync" {rsync_opts}'

        host_str = self._host_for_ssh(c.host)
        command = f'{self.rsync_command} {rsync_opts} {ssh_opts} {self.src_dir_or_file} {host_str}:{self.dst_dir}'

        return localhost_connection.run(command, hide=False, timeout=self.rsync_timeout)


__all__ = (
    "GetFile",
    "PutFile",
    "PutTemplate",
    "Rsync",
)
