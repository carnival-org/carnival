from typing import List, Optional

from carnival import cmd
from carnival.host.connection import Connection


def get_pkg_versions(c: Connection, pkgname: str) -> List[str]:
    """
    Получить список доступных версий пакета
    """
    versions = []
    result = cmd.cli.run(c, f"DEBIAN_FRONTEND=noninteractive apt-cache madison {pkgname}", hide=True, warn=True)
    if result.ok is False:
        return []

    for line in result.stdout.strip().split("\n"):
        n, ver, r = line.split("|")
        versions.append(ver.strip())
    return versions


def get_installed_version(c: Connection, pkgname: str) -> Optional[str]:
    """
    Получить установленную версию пакета

    :return: Версия пакета если установлен, `None` если пакет не установлен
    """
    result = cmd.cli.run(c, f"DEBIAN_FRONTEND=noninteractive dpkg -l {pkgname}", hide=True, warn=True)
    if result.ok is False:
        return None
    installed, pkgn, ver, arch, *desc = result.stdout.strip().split("\n")[-1].split()
    if installed != 'ii':
        return None

    assert isinstance(ver, str)
    return ver.strip()


def is_pkg_installed(c: Connection, pkgname: str, version: Optional[str] = None) -> bool:
    """
    Проверить установлен ли пакет
    Если версия не указана - проверяется любая
    """

    pkgver = get_installed_version(c, pkgname)
    if version is None and pkgver is not None:
        return True

    if version is not None and pkgver == version:
        return True

    return False


def force_install(c: Connection, pkgname: str, version: Optional[str] = None, update: bool = False, hide: bool = False) -> None:
    """
    Установить пакет без проверки установлен ли он
    """
    if version:
        pkgname = f"{pkgname}={version}"

    if update:
        cmd.cli.run(c, "DEBIAN_FRONTEND=noninteractive sudo apt-get update", hide=hide)

    cmd.cli.run(c, f"DEBIAN_FRONTEND=noninteractive sudo apt-get install -y {pkgname}", hide=hide)


def install(c: Connection, pkgname: str, version: Optional[str] = None, update: bool = True, hide: bool = False,) -> bool:
    """
    Установить пакет если он еще не установлен в системе

    :param pkgname: название пакета
    :param version: версия
    :param update: запустить apt-get update перед установкой
    :param hide: скрыть вывод этапов
    :return: `True` если пакет был установлен, `False` если пакет уже был установлен ранее
    """
    if is_pkg_installed(c, pkgname, version):
        if version:
            if not hide:
                print(f"{pkgname}={version} already installed")
        else:
            if not hide:
                print(f"{pkgname} already installed")
        return False
    force_install(c, pkgname=pkgname, version=version, update=update, hide=hide)
    return True


def install_multiple(c: Connection, *pkg_names: str, update: bool = True, hide: bool = False) -> bool:
    """
    Установить несколько пакетов, если они не установлены

    :param pkg_names: список пакетов которые нужно установить
    :param update: запустить apt-get update перед установкой
    :param hide: скрыть вывод этапов
    :return: `True` если хотя бы один пакет был установлен, `False` если все пакеты уже были установлен ранее
    """
    if all([is_pkg_installed(c, x) for x in pkg_names]):
        if not hide:
            print(f"{','.join(pkg_names)} already installed")
        return False

    if update:
        cmd.cli.run(c, "DEBIAN_FRONTEND=noninteractive sudo apt-get update", hide=hide)

    for pkg in pkg_names:
        install(c, pkg, update=False, hide=hide)
    return True


def remove(c: Connection, *pkg_names: str, hide: bool = False) -> None:
    """
    Удалить пакет

    :param pkg_names: список пакетов которые нужно удалить
    :param hide: скрыть вывод этапов
    """
    assert pkg_names, "pkg_names is empty"
    cmd.cli.run(c, f"DEBIAN_FRONTEND=noninteractive sudo apt-get remove --auto-remove -y {' '.join(pkg_names)}", hide=hide)
