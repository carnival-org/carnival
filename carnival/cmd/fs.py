from typing import List, Optional
import re

from carnival import cmd
from carnival.host import AnyConnection

from invoke import Result  # type: ignore


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


def mkdirs(c: AnyConnection, *dirs: str) -> List[Result]:
    """
    Создать директории

    :param dirs: пути которые нужно создать
    """
    return [cmd.cli.run(c, f"mkdir -p {x}", hide=True) for x in dirs]


def is_dir_exists(c: AnyConnection, dir_path: str) -> bool:
    """
    Узнать существует ли директория

    :param dir_path: путь до директории
    """
    return bool(cmd.cli.run(c, f"test -d {dir_path}", warn=True, hide=True).ok)


def is_file_contains(c: AnyConnection, filename: str, text: str, exact: bool = False, escape: bool = True) -> bool:
    """
    Содержит ли файл текст

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
    return c.run(egrep_cmd, hide=True, warn=True).ok  # type: ignore


def is_file_exists(c: AnyConnection, path: str) -> bool:
    """
    Проверить существует ли файл

    :param path: путь до файла
    """

    cmd = 'test -e "$(echo {})"'.format(path)
    return c.run(cmd, hide=True, warn=True).ok  # type: ignore


def ensure_dir_exists(
    c: AnyConnection,
    path: str,
    user: Optional[str] = None,
    group: Optional[str] = None,
    mode: Optional[str] = None,
) -> None:
    """
    Проверить что директория существует и параметры соответствуют заданным

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
