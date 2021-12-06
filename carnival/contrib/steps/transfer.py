import os.path
import typing
from io import BytesIO
from hashlib import sha1

from tqdm import tqdm  # type: ignore
from colorama import Style as S, Fore as F  # type: ignore

from carnival import Connection, localhost_connection
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
                validators.IsDirectoryValidator(self.local_path, on_localhost=True),
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
            validators.IsFileValidator(self.local_path, on_localhost=True),
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


__all__ = (
    "GetFile",
    "PutFile",
    "PutTemplate",
)
