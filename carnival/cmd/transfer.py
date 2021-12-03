from io import BytesIO
from typing import Any
from hashlib import sha1

from colorama import Fore as F, Style as S  # type: ignore

from carnival import Connection, Result, SshHost, Host, cmd
from carnival.hosts.local import localhost_connection
from carnival.templates import render


from fabric.transfer import Transfer  # type:ignore
from paramiko.config import SSH_PORT


def _get_ssh_host_addess_for_ssh_cli(host: SshHost) -> str:
    """
    Return `user@addr` if user given, else `addr`
    """

    if host.ssh_user:
        return f"{host.ssh_user}@{host.addr}"
    return host.addr


def rsync(
    host: Host,
    source: str,
    target: str,

    rsync_opts: str = "--progress -pthrvz --timeout=60",
    ssh_opts: str = '',
    rsync_command: str = "rsync",
    hide: bool = False,
) -> Result:
    """
    Залить папку с локального диска на сервер по rsync

    :param host: сервер куда заливать
    :param source: локальный путь до папки
    :param target: путь куда нужно залить
    :param rsync_opts: параметры команды rsync
    :param ssh_opts: параметры ssh
    :param rsync_command: путь до rsync
    :param hide: скрыть результаты выполнения
    """

    assert isinstance(host, SshHost)  # TODO: Think about remove this

    if host.ssh_port != SSH_PORT:
        ssh_opts = f"-p {host.ssh_port} {ssh_opts}"

    if host.ssh_gateway is not None:
        if host.ssh_gateway.ssh_gateway is not None:
            raise ValueError("gateway for gateway s not supported for rsync, please use .ssh/config")
        ssh_opts = f"-J {_get_ssh_host_addess_for_ssh_cli(host.ssh_gateway)}:{host.ssh_gateway.ssh_port}"

    ssh_opts = ssh_opts.strip()
    if ssh_opts:
        ssh_opts = f'-e "ssh {ssh_opts.strip()}"'

    command = f'{rsync_command} {rsync_opts} {ssh_opts} {source} {_get_ssh_host_addess_for_ssh_cli(host)}:{target}'

    return localhost_connection.run(command, hide=hide)


def get(c: Connection, remote: str, local: str, preserve_mode: bool = True) -> None:
    """
    Скачать файл с сервера
    <http://docs.fabfile.org/en/2.5/api/transfer.html#fabric.transfer.Transfer.get>

    :param c: Конект с хостом
    :param remote: путь до файла на сервере
    :param local: путь куда сохранить файл
    :param preserve_mode: сохранить права
    """
    # TODO: c._c ;(
    t = Transfer(c._c)  # type: ignore
    t.get(remote=remote, local=local, preserve_mode=preserve_mode)


def put(c: Connection, local: str, remote: str, preserve_mode: bool = True) -> None:
    """
    Закачать файл на сервер
    <http://docs.fabfile.org/en/2.5/api/transfer.html#fabric.transfer.Transfer.put>

    :param c: Конект с хостом
    :param local: путь до локального файла
    :param remote: путь куда сохранить на сервере
    :param preserve_mode: сохранить права
    """
    # TODO: c._c ;(
    t = Transfer(c._c)  # type: ignore
    t.put(local=local, remote=remote, preserve_mode=preserve_mode)


def put_template(c: Connection, template_path: str, remote: str, **context: Any) -> bool:
    """
    Отрендерить файл с помощью jinja-шаблонов и закачать на сервер
    См раздел templates.

    <http://docs.fabfile.org/en/2.5/api/transfer.html#fabric.transfer.Transfer.put>

    :param c: Конект с хостом
    :param template_path: путь до локального файла jinja
    :param remote: путь куда сохранить на сервере
    :param context: контекс для рендеринга jinja2
    """
    filestr = render(template_path=template_path, **context)

    shasum_exist = cmd.cli.is_cmd_exist(c, "shasum")
    if shasum_exist is False:
        print(f"{F.YELLOW}[WARN]{F.RESET} shasum is not found on remote, lazy uploading is not possible")
        is_remote_exists = True

    if shasum_exist:
        is_remote_exists = cmd.fs.is_file_exists(c, remote)
        if is_remote_exists:
            # Check hashed to prevent unneeded upload
            filestr_hash = sha1(filestr.encode()).hexdigest()
            remotehash_result = c.run(f"cat {remote} | shasum -a1", hide=True).stdout.strip(" -\t\n")
            if filestr_hash == remotehash_result:
                print(f"{S.BRIGHT}{template_path}{S.RESET_ALL}: {F.GREEN}not changed{F.RESET}")
                return False

    # TODO: c._c ;(
    t = Transfer(c._c)  # type: ignore
    t.put(local=BytesIO(filestr.encode()), remote=remote, preserve_mode=False)

    if is_remote_exists:
        print(f"{S.BRIGHT}{template_path}{S.RESET_ALL}: {F.YELLOW}updated{F.RESET}")
    else:
        print(f"{S.BRIGHT}{template_path}{S.RESET_ALL}: {F.YELLOW}created{F.RESET}")

    return True
