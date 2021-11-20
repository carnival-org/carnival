import typing
from io import BytesIO
from tqdm import tqdm  # type:ignore

from carnival.templates import render
from carnival.host.connection import Connection


def putfo(
    reader: typing.IO[bytes],
    dst: Connection, dst_file_path: str,
    dst_file_size: int,
    bufsize: int = 32768,
) -> None:
    write_size = 0

    with tqdm(desc=f"Transferring {dst_file_path}", unit='B', unit_scale=True, total=dst_file_size) as pbar:
        with dst.file_write(dst_file_path) as writer:
            while True:
                data = reader.read(bufsize)
                if len(data) == 0:
                    break

                writer.write(data)
                pbar.update(len(data))
                write_size += len(data)

    if dst_file_size != write_size:
        raise IOError(f"size mismatch! {dst_file_size} != {write_size}")


def getfo(
    src: Connection, src_file_path: str,
) -> typing.ContextManager[typing.IO[bytes]]:
    return src.file_read(src_file_path)


def transfer(
    src: Connection, src_file_path: str,
    dst: Connection, dst_file_path: str,
    preserve_mode: bool = True,
) -> None:
    """
    Скачать файл с сервера
    <http://docs.fabfile.org/en/2.5/api/transfer.html#fabric.transfer.Transfer.get>

    :param remote: путь до файла на сервере
    :param local: путь куда сохранить файл
    :param preserve_mode: сохранить права
    """
    file_size = src.file_stat(src_file_path).st_size

    with src.file_read(src_file_path) as reader:
        putfo(
            reader,
            dst=dst, dst_file_path=dst_file_path,
            dst_file_size=file_size,
        )


def put_template(
    template_path: str,
    dst: Connection,
    dst_path: str,
    **context: typing.Any,
) -> None:
    """
    Отрендерить файл с помощью jinja-шаблонов и закачать на сервер
    См раздел templates.

    <http://docs.fabfile.org/en/2.5/api/transfer.html#fabric.transfer.Transfer.put>

    :param template_path: путь до локального файла jinja
    :param dst: connection-обьект с сервером назначения
    :param dst_path: путь куда сохранить на сервере
    :param context: контекс для рендеринга jinja2
    """
    filestr = render(template_path=template_path, **context)
    putfo(
        BytesIO(filestr.encode()),
        dst=dst, dst_file_path=dst_path,
        dst_file_size=len(filestr),
    )
