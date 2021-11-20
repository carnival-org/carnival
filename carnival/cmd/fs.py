import typing
import re

from carnival import cmd
from carnival.host.connection import Connection, Result


def mkdirs(c: Connection, dirs: typing.List[str]) -> typing.List[Result]:
    """
    Создать директории

    :param dirs: пути которые нужно создать
    """
    return [cmd.cli.run(c, f"mkdir -p {x}", hide=True) for x in dirs]


def is_dir_exists(c: Connection, dir_path: str) -> bool:
    """
    Узнать существует ли директория

    :param dir_path: путь до директории
    """
    return bool(cmd.cli.run(c, f"test -d {dir_path}", warn=True, hide=True).ok)


def is_file_contains(c: Connection, filename: str, text: str) -> bool:
    """
    Содержит ли файл текст

    :param filename: путь до файла
    :param text: текст который нужно искать
    :param exact: точное совпадение
    :param escape: экранировать ли текст
    """

    # Escape for regex
    text = re.escape(text).replace("\\\\", "\\\\\\").replace(r"\$", r"\\\$").replace(r"\'", "'")
    egrep_cmd = f'egrep "{text}" "{filename}"'
    return cmd.cli.run(c, egrep_cmd, hide=True, warn=True).ok


def is_file_exists(c: Connection, path: str) -> bool:
    """
    Проверить существует ли файл

    :param path: путь до файла
    """
    command = f'test -e "$(echo {path})"'
    return cmd.cli.run(c, command, hide=True, warn=True).ok
