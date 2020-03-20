from typing import List
import os

from invoke import Result  # type: ignore

from carnival import cmd


def set_password(username: str, password: str) -> Result:
    """
    Установить пароль пользователю

    :param username: Пользователь
    :param password: Новый пароль
    """
    return cmd.cli.pty(f"echo '{username}:{password}' | chpasswd", hide=True)


def ssh_authorized_keys_add(ssh_key: str, keys_file=".ssh/authorized_keys") -> bool:
    """
    Добавить ssh ключ в `authorized_keys`

    :param ssh_key: ключ
    :param keys_file: пусть до файла `authorized_keys`
    :return: `True` если ключ был добавлен, `False` если ключ уже был в файле
    """
    ssh_key = ssh_key.strip()

    cmd.cli.run("mkdir -p ~/.ssh")
    cmd.cli.run("chmod 700 ~/.ssh")
    cmd.cli.run(f"touch {keys_file}")

    if not cmd.fs.is_file_contains(keys_file, ssh_key, escape=True):
        cmd.cli.run(f"echo '{ssh_key}' >> {keys_file}")
        return True
    return False


def ssh_authorized_keys_list() -> List[str]:
    """
    Получить список авторизованных ssh-ключей сервера
    """
    if cmd.fs.is_file_exists("~/.ssh/authorized_keys") is False:
        return []

    return cmd.cli.run("cat ~/.ssh/authorized_keys", hide=True).stdout.strip().split("\n")


def ssh_authorized_keys_ensure(*ssh_keys: str) -> List[bool]:
    """
    Добавить несколько ssh-ключей в авторизованные

    :param ssh_keys: ssh-ключи
    :return: Список `True` если ключ был добавлен, `False` если ключ уже был в файле
    """
    return [ssh_authorized_keys_add(x) for x in ssh_keys]


def ssh_copy_id(pubkey_file="~/.ssh/id_rsa.pub") -> bool:
    """
    Добавить публичный ssh-ключ текущего пользователя в авторизованные

    :param pubkey_file: путь до файла с публичным ключем
    :return: `True` если ключ был добавлен, `False` если ключ уже был в файле
    """
    return ssh_authorized_keys_add(open(os.path.expanduser(pubkey_file)).read().strip())


def get_current_user_name() -> str:
    """
    Получить имя текущего пользователя
    """
    return cmd.cli.run("id -u -n", hide=True).stdout.strip()


def get_current_user_id() -> int:
    """
    Получить id текущего пользователя
    """
    return int(cmd.cli.run("id -u", hide=True).stdout.strip())


def is_current_user_root() -> bool:
    """
    Проверить что текущий пользователь - `root`
    """
    return get_current_user_id() == 0
