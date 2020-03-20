from typing import List

from patchwork import files  # type:ignore
from invoke import Result  # type: ignore

from carnival import cmd

from carnival import global_context


def mkdirs(*dirs: str) -> List[Result]:
    """
    Создать директории

    :param dirs: пути которые нужно создать
    """
    return [cmd.cli.run(f"mkdir -p {x}", hide=True) for x in dirs]


def is_dir_exists(dir_path: str) -> bool:
    """
    Узнать существует ли директория

    :param dir_path: путь до директории
    """
    return cmd.cli.run(f"test -d {dir_path}", warn=True, hide=True).ok


def is_file_contains(filename, text, exact=False, escape=True) -> bool:
    """
    Содержит ли файл текст
    См <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.contains>

    :param filename: путь до файла
    :param text: текст который нужно искать
    :param exact: точное совпадение
    :param escape: экранировать ли текст


    """

    return files.contains(global_context.conn, runner=global_context.conn.run, filename=filename, text=text, exact=exact, escape=escape)


def is_file_exists(path) -> bool:
    """
    Проверить существует ли файл
    <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.exists>

    :param path: путь до файла
    """
    return files.exists(global_context.conn, runner=global_context.conn.run, path=path)


def ensure_dir_exists(path, user=None, group=None, mode=None) -> None:
    """
    Проверить что директория существует и параметры соответствуют заданным

    <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.directory>

    :param path: путь до директории
    :param user: владелец
    :param group: группа
    :param mode: права
    """
    files.directory(global_context.conn, runner=global_context.conn.run, path=path, user=user, group=group, mode=mode)
