from carnival import cmd
from carnival import Connection, Result


def set_password(c: Connection, username: str, password: str) -> Result:
    """
    Установить пароль пользователю

    :param username: Пользователь
    :param password: Новый пароль
    """
    return cmd.cli.run(c, f"echo '{username}:{password}' | chpasswd", hide=True)


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
