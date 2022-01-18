"""
Хелперы для помощи в написании шагов (Steps)
"""

import typing
import re

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


def get_user_id(c: Connection) -> int:
    """
    Получить id пользователя под которым запущено соединение
    Если соединение с sudo то получить id пользователя под которым sudo
    """
    result = c.run("id -u")
    return int(result.stdout.strip())


def get_user_group_id(c: Connection) -> int:
    """
    Получить group id пользователя под которым запущено соединение
    Если соединение с sudo то получить group id пользователя под которым sudo
    """
    result = c.run("id -g")
    return int(result.stdout.strip())


def _escape_for_regex(text: str) -> str:
    """
    Tnx to https://stackoverflow.com/questions/280435/escaping-regex-string
    :param text:
    :return:
    """
    regex = re.escape(text)
    # double escaping for \
    regex = regex.replace("\\\\", "\\\\\\")
    # triple-escaping for $ signs
    regex = regex.replace(r"\$", r"\\\$")
    # single quotes should not be escaped
    regex = regex.replace(r"\'", "'")
    return regex


def is_file_contains(c: Connection, filename: str, text: str, escape: bool = True) -> bool:
    """
    Содержит ли файл текст

    :param c: Конект с хостом
    :param filename: путь до файла
    :param text: текст который нужно искать
    :param escape: экранировать ли текст
    """
    if escape:
        text = _escape_for_regex(text)
    egrep_cmd = f'egrep "{text}" {filename}'
    return c.run(egrep_cmd, hide=True, warn=True, use_sudo=False).ok


def append_string_to_file(c: Connection, file: str, string: str, use_sudo: typing.Optional[bool] = None) -> None:
    """
    Дописать строку в конец файла
    """
    c.run(f'echo "{string}" >> {file}', use_sudo=use_sudo)
