import typing

from carnival import cmd
from carnival.host.connection import Connection, Result
from patchwork import files  # type: ignore


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


def is_file_contains(c: Connection, filename: str, text: str, exact: bool = False, escape: bool = True) -> bool:
    """
    Содержит ли файл текст
    См <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.contains>

    :param filename: путь до файла
    :param text: текст который нужно искать
    :param exact: точное совпадение
    :param escape: экранировать ли текст
    """

    return bool(files.contains(
        c,
        runner=c.run,
        filename=filename, text=text, exact=exact, escape=escape
    ))


def is_file_exists(c: Connection, path: str) -> bool:
    """
    Проверить существует ли файл
    <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.exists>

    :param path: путь до файла
    """
    return bool(files.exists(c, runner=c.run, path=path))


def ensure_dir_exists(
    c: Connection,
    path: str,
    user: typing.Optional[str] = None,
    group: typing.Optional[str] = None,
    mode: typing.Optional[str] = None,
) -> None:
    """
    Проверить что директория существует и параметры соответствуют заданным

    <https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.directory>

    :param path: путь до директории
    :param user: владелец
    :param group: группа
    :param mode: права
    """
    files.directory(c, runner=c.run, path=path, user=user, group=group, mode=mode)
