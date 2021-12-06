import os.path
import typing
from io import BytesIO
from hashlib import sha1

from tqdm import tqdm  # type: ignore
from colorama import Style as S, Fore as F  # type: ignore
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
    writer: typing.IO[bytes],
    dst_file_size: int,
    dst_file_path: str,
    bufsize: int = 32768,
) -> None:
    write_size = 0

    with tqdm(
        desc=f"Transferring {dst_file_path}",
            unit='B', unit_scale=True, total=dst_file_size,
            leave=False,
    ) as pbar:
        while True:
            data = reader.read(bufsize)
            if len(data) == 0:
                break

            writer.write(data)
            pbar.update(len(data))
            write_size += len(data)

    if dst_file_size != write_size:
        raise IOError(f"size mismatch! {dst_file_size} != {write_size}")


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

        # Create dirs if needed
        dirname = os.path.dirname(self.local_path)
        if dirname:
            localhost_connection.run(f"mkdir -p {dirname}", hide=True)

        with localhost_connection.file_write(self.local_path) as writer:
            with c.file_read(self.remote_path) as reader:
                dst_file_size = c.file_stat(self.remote_path).st_size
                _transfer_file(
                    reader=reader, writer=writer,
                    dst_file_size=dst_file_size, dst_file_path=self.remote_path,
                )

        print(f"{S.BRIGHT}{self.remote_path}{S.RESET_ALL}: {F.YELLOW}downloaded{F.RESET}")


class PutFile(Step):
    """
    Закачать файл на сервер

    """
    def __init__(self, local_path: str, remote_path: str, ):
        """
        :param local_path: путь до локального файла
        :param remote_path: путь куда сохранить на сервере
        """
        self.local_path = local_path
        self.remote_path = remote_path

    def get_name(self) -> str:
        return f"{super().get_name()}(local_path={self.local_path}, remote_path={self.remote_path})"

    def get_validators(self) -> typing.List["validators.StepValidatorBase"]:
        return [
            validators.Local(validators.IsFileValidator(self.local_path)),
            validators.Not(
                validators.IsDirectoryValidator(self.remote_path),
                error_message=f"{self.remote_path} must be full file path, not directory",
            )
        ]

    def run(self, c: "Connection") -> None:
        remote_sha1 = _file_sha1sum(c, self.remote_path)
        local_sha1 = _file_sha1sum(localhost_connection, self.local_path)
        if remote_sha1 is not None and local_sha1 is not None:
            if remote_sha1 == local_sha1:
                return

        # Create dirs if needed
        dirname = os.path.dirname(self.remote_path)
        if dirname:
            c.run(f"mkdir -p {dirname}", hide=True)

        with localhost_connection.file_read(self.local_path) as reader:
            with c.file_write(self.remote_path) as writer:
                dst_file_size = localhost_connection.file_stat(self.local_path).st_size
                _transfer_file(
                    reader=reader, writer=writer,
                    dst_file_size=dst_file_size, dst_file_path=self.remote_path,
                )

        print(f"{S.BRIGHT}{self.remote_path}{S.RESET_ALL}: {F.YELLOW}uploaded{F.RESET}")


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

        # Create dirs if needed
        dirname = os.path.dirname(self.remote_path)
        if dirname:
            c.run(f"mkdir -p {dirname}", hide=True)

        with c.file_write(self.remote_path) as writer:
            _transfer_file(
                reader=BytesIO(filebytes), writer=writer,
                dst_file_size=len(filebytes), dst_file_path=self.remote_path,
            )

        print(f"{S.BRIGHT}{self.remote_path}{S.RESET_ALL}: {F.YELLOW}uploaded{F.RESET}")


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

        if host.ssh_user:
            return f"{host.ssh_user}@{host.addr}"
        return host.addr

    @staticmethod
    def _validate_dst_host_double_gateway(c: Connection) -> bool:
        assert isinstance(c.host, SshHost)
        if c.host.ssh_gateway is not None:
            if c.host.ssh_gateway.ssh_gateway is not None:
                return True
        return False

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.InlineValidator(
                lambda c: not isinstance(c.host, SshHost),
                "remote host must be ssh connected host",
            ),
            validators.InlineValidator(
                self._validate_dst_host_double_gateway,
                "gateway for gateway s not supported for rsync, please use .ssh/config",
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

        # Ensure dir exists
        c.run(f"mkdir -p {self.dst_dir}", hide=True)

        ssh_opts = self.ssh_opts

        if c.host.ssh_port != SSH_PORT:
            ssh_opts = f"-p {c.host.ssh_port} {ssh_opts}"

        if c.host.ssh_gateway is not None:
            ssh_opts = f"-J {self._host_for_ssh(c.host.ssh_gateway)}:{c.host.ssh_gateway.ssh_port}"

        ssh_opts = ssh_opts.strip()
        if ssh_opts:
            ssh_opts = f'-e "ssh {ssh_opts.strip()}"'

        host_str = self._host_for_ssh(c.host)
        command = f'{self.rsync_command} {self.rsync_opts} {ssh_opts} {self.src_dir_or_file} {host_str}:{self.dst_dir}'

        return localhost_connection.run(command, hide=False, timeout=self.rsync_timeout)


__all__ = (
    "GetFile",
    "PutFile",
    "PutTemplate",
    "Rsync",
)
