from typing import List, Optional

from carnival import cmd, connection
from invoke import Result  # type: ignore
from patchwork import files  # type:ignore


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
    return bool(cmd.cli.run(f"test -d {dir_path}", warn=True, hide=True).ok)


def is_file_contains(filename: str, text: str, exact: bool = False, escape: bool = True) -> bool:
    """
    Содержит ли файл текст
    См <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.contains>

    :param filename: путь до файла
    :param text: текст который нужно искать
    :param exact: точное совпадение
    :param escape: экранировать ли текст


    """
    assert connection.conn is not None, "No connection"
    return bool(files.contains(
        connection.conn,
        runner=connection.conn.run,
        filename=filename, text=text, exact=exact, escape=escape
    ))


def is_file_exists(path: str) -> bool:
    """
    Проверить существует ли файл
    <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.exists>

    :param path: путь до файла
    """
    assert connection.conn is not None, "No connection"
    return bool(files.exists(connection.conn, runner=connection.conn.run, path=path))


def ensure_dir_exists(
    path: str,
    user: Optional[str] = None,
    group: Optional[str] = None,
    mode: Optional[str] = None,
) -> None:
    """
    Проверить что директория существует и параметры соответствуют заданным

    <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.directory>

    :param path: путь до директории
    :param user: владелец
    :param group: группа
    :param mode: права
    """
    assert connection.conn is not None, "No connection"
    files.directory(connection.conn, runner=connection.conn.run, path=path, user=user, group=group, mode=mode)
