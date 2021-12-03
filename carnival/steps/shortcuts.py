"""
Хелперы для помощи в написании шагов (Steps)
"""

from carnival import Connection, Result, SshHost, Host
from carnival.hosts.local import localhost_connection

from paramiko.config import SSH_PORT


def is_file(c: Connection, path: str) -> bool:
    """
    Проверить существует ли файл

    :param c: Конект с хостом
    :param path: путь до файла
    """

    return c.run(f'test -e "$(echo {path})"', hide=True, warn=True).ok


def is_directory(c: Connection, path: str) -> bool:
    """
    Проверить существует ли директория

    :param c: Конект с хостом
    :param path: путь до директории
    """

    return c.run(f'test -d "$(echo {path})"', hide=True, warn=True).ok


def is_cmd_exist(c: Connection, cmd_name: str) -> bool:
    """
    Проверить есть ли команда в $PATH

    :param c: Конект с хостом
    :param cmd_name: Команда
    """
    return c.run(f"which {cmd_name}", hide=True, warn=True).ok


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
