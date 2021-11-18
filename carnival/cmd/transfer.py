from io import BytesIO
import typing

from paramiko.config import SSH_PORT
from tqdm import tqdm  # type: ignore

from carnival.templates import render
from carnival.host import SSHHost, SSHConnection, AnyConnection
from carnival.host import Result
from carnival.host import localhost


def _pbar_update(pbar: tqdm, x: int, y: int) -> None:
    pbar.total = y
    pbar.n = x
    pbar.refresh()


def rsync(
    host: SSHHost,
    source: str,
    target: str,

    rsync_opts: str = "--progress -pthrvz --timeout=60",
    ssh_opts: str = '',
    rsync_command: str = "rsync",
    hide: bool = False,
) -> Result:
    """
    Залить папку с локального диска на сервер по rsync

    :param host: сервер
    :param source: локальный путь до папки
    :param target: путь куда нужно залить
    :param rsync_opts: параметры команды rsync
    :param ssh_opts: параметры ssh
    :param rsync_command: путь до rsync
    :param hide: скрыть результаты выполнения
    """

    if host.port != SSH_PORT:
        ssh_opts = f"-p {host.port} {ssh_opts}"

    if host.ssh_gateway is not None:
        if host.ssh_gateway.ssh_gateway is not None:
            raise ValueError("gateway for gateway s not supported for rsync, please use .ssh/config")
        ssh_opts = f"-J {host.ssh_gateway.get_ssh_addess()}:{host.ssh_gateway.port}"

    ssh_opts = ssh_opts.strip()
    if ssh_opts:
        ssh_opts = f'-e "ssh {ssh_opts.strip()}"'

    command = f'{rsync_command} {rsync_opts} {ssh_opts} {source} {host.get_ssh_addess()}:{target}'

    with localhost.connect() as local_conn:
        result_promise = local_conn.run(command, hide=hide)
        return result_promise.wait()


def get(c: SSHConnection, remote: str, local: str) -> None:
    """
    Скачать файл с сервера

    :param remote: путь до файла на сервере
    :param local: путь куда сохранить файл
    :param preserve_mode: сохранить права
    """
    with c.conn.open_sftp() as sftp:
        with tqdm(desc=f"Downloading {remote}", unit='B', unit_scale=True) as pbar:
            sftp.get(remotepath=remote, localpath=local, callback=lambda x, y: _pbar_update(pbar, x, y))


def put(c: SSHConnection, local: str, remote: str) -> None:
    """
    Закачать файл на сервер

    :param local: путь до локального файла
    :param remote: путь куда сохранить на сервере
    :param preserve_mode: сохранить права
    """
    with c.conn.open_sftp() as sftp:
        with tqdm(desc=f"Uploading {remote}", unit='B', unit_scale=True) as pbar:
            sftp.put(localpath=local, remotepath=remote, confirm=True, callback=lambda x, y: _pbar_update(pbar, x, y))


def put_template(c: SSHConnection, template_path: str, remote: str, **context: typing.Any) -> None:
    """
    Отрендерить файл с помощью jinja-шаблонов и закачать на сервер
    См раздел templates.

    :param template_path: путь до локального файла jinja
    :param remote: путь куда сохранить на сервере
    :param context: контекс для рендеринга jinja2
    """
    filestr = render(template_path=template_path, **context)

    with c.conn.open_sftp() as sftp:
        with tqdm(desc=f"Uploading {template_path}", unit='B', unit_scale=True) as pbar:
            sftp.putfo(
                fl=BytesIO(filestr.encode()), remotepath=remote,
                confirm=True,
                callback=lambda x, y: _pbar_update(pbar, x, y)
            )


def _is_path_exists(c: AnyConnection, filepath: str) -> bool:
    promise = c.run(f"test -e {filepath}", hide=False)
    result = promise.wait()
    return result.ok
