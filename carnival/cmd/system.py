import typing

from carnival import cmd
from carnival.host.connection import Result, Connection


def set_password(c: Connection, username: str, password: str) -> Result:
    """
    Установить пароль пользователю

    :param username: Пользователь
    :param password: Новый пароль
    """
    return cmd.cli.run(c, f"echo '{username}:{password}' | chpasswd", hide=True)


def ssh_authorized_keys_add(c: Connection, ssh_key: str, keys_file: str = ".ssh/authorized_keys") -> bool:
    """
    Добавить ssh ключ в `authorized_keys`

    :param ssh_key: ключ
    :param keys_file: пусть до файла `authorized_keys`
    :return: `True` если ключ был добавлен, `False` если ключ уже был в файле
    """
    ssh_key = ssh_key.strip()

    cmd.cli.run(c, "mkdir -p ~/.ssh")
    cmd.cli.run(c, "chmod 700 ~/.ssh")
    cmd.cli.run(c, f"touch {keys_file}")

    if not cmd.fs.is_file_contains(c, keys_file, ssh_key):
        cmd.cli.run(c, f"echo '{ssh_key}' >> {keys_file}")
        return True
    return False


def ssh_authorized_keys_list(c: Connection) -> typing.List[str]:
    """
    Получить список авторизованных ssh-ключей сервера
    """
    if cmd.fs.is_file_exists(c, "~/.ssh/authorized_keys") is False:
        return []

    keys_file: str = cmd.cli.run(c, "cat ~/.ssh/authorized_keys", hide=True).stdout.strip()
    return keys_file.split("\n")


def ssh_authorized_keys_ensure(c: Connection, ssh_keys: typing.List[str]) -> typing.List[bool]:
    """
    Добавить несколько ssh-ключей в авторизованные

    :param ssh_keys: ssh-ключи
    :return: Список `True` если ключ был добавлен, `False` если ключ уже был в файле
    """
    return [ssh_authorized_keys_add(c, x) for x in ssh_keys]


def get_current_user_name(c: Connection) -> str:
    """
    Получить имя текущего пользователя
    """
    id_res: str = cmd.cli.run(c, "id -u -n", hide=True).stdout
    return id_res.strip()


def get_current_user_id(c: Connection) -> int:
    """
    Получить id текущего пользователя
    """
    return int(cmd.cli.run(c, "id -u", hide=True).stdout.strip())


def is_current_user_root(c: Connection) -> bool:
    """
    Проверить что текущий пользователь - `root`
    """
    return get_current_user_id(c) == 0
