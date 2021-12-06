"""
Хелперы для помощи в написании шагов (Steps)
"""

from carnival import Connection


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
