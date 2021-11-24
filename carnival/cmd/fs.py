from typing import List, Optional
import re

from carnival import cmd
from carnival import Connection, Result


def _escape_for_regex(text: str) -> str:
    """Escape ``text`` to allow literal matching using egrep"""
    regex = re.escape(text)
    # Seems like double escaping is needed for \
    regex = regex.replace("\\\\", "\\\\\\")
    # Triple-escaping seems to be required for $ signs
    regex = regex.replace(r"\$", r"\\\$")
    # Whereas single quotes should not be escaped
    regex = regex.replace(r"\'", "'")
    return regex


def mkdirs(c: Connection, *dirs: str) -> List[Result]:
    """
    Создать директории

    :param c: Конект с хостом
    :param dirs: пути которые нужно создать
    """
    return [cmd.cli.run(c, f"mkdir -p {x}", hide=True) for x in dirs]


def is_dir_exists(c: Connection, dir_path: str) -> bool:
    """
    Узнать существует ли директория

    :param c: Конект с хостом
    :param dir_path: путь до директории
    """
    return bool(cmd.cli.run(c, f"test -d {dir_path}", warn=True, hide=True).ok)


def is_file_contains(c: Connection, filename: str, text: str, exact: bool = False, escape: bool = True) -> bool:
    """
    Содержит ли файл текст

    :param c: Конект с хостом
    :param filename: путь до файла
    :param text: текст который нужно искать
    :param exact: точное совпадение
    :param escape: экранировать ли текст


    """
    if escape:
        text = _escape_for_regex(text)
        if exact:
            text = "^{}$".format(text)
    egrep_cmd = 'egrep "{}" "{}"'.format(text, filename)
    return c.run(egrep_cmd, hide=True, warn=True).ok


def is_file_exists(c: Connection, path: str) -> bool:
    """
    Проверить существует ли файл

    :param c: Конект с хостом
    :param path: путь до файла
    """

    cmd = 'test -e "$(echo {})"'.format(path)
    return c.run(cmd, hide=True, warn=True).ok


def ensure_dir_exists(
    c: Connection,
    path: str,
    user: Optional[str] = None,
    group: Optional[str] = None,
    mode: Optional[str] = None,
) -> None:
    """
    Проверить что директория существует и параметры соответствуют заданным

    :param c: Конект с хостом
    :param path: путь до директории
    :param user: владелец
    :param group: группа
    :param mode: права
    """

    c.run("mkdir -p {}".format(path))
    if user is not None:
        group = group or user
        c.run("chown {}:{} {}".format(user, group, path))
    if mode is not None:
        c.run("chmod {} {}".format(mode, path))
