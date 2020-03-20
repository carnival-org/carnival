from typing import Optional, List

from carnival import cmd
from carnival.utils import log


def get_pkg_versions(pkgname: str) -> List[str]:
    """
    Получить список доступных версий пакета
    """
    versions = []
    result = cmd.cli.run(f"apt-cache madison {pkgname}", hide=True, warn=True)
    if result.ok is False:
        return []

    for line in result.stdout.strip().split("\n"):
        n, ver, r = line.split("|")
        versions.append(ver.strip())
    return versions


def get_installed_version(pkgname: str) -> Optional[str]:
    """
    Получить установленную версию пакета

    :return: Версия пакета если установлен, `None` если пакет не установлен
    """
    result = cmd.cli.run(f"dpkg -l {pkgname}", hide=True, warn=True)
    if result.ok is False:
        return None
    installed, pkgn, ver, arch, *desc = result.stdout.strip().split("\n")[-1].split()
    if installed != 'ii':
        return None
    return ver.strip()


def is_pkg_installed(pkgname: str, version=None) -> bool:
    """
    Проверить установлен ли пакет
    Если версия не указана - проверяется любая
    """

    pkgver = get_installed_version(pkgname)
    if version is None and pkgver is not None:
        return True

    if version is not None and pkgver == version:
        return True

    return False


def force_install(pkgname, version=None, update=False, hide=False):
    """
    Установить пакет без проверки установлен ли он
    """
    if version:
        pkgname = f"{pkgname}={version}"

    if update:
        cmd.cli.run("sudo apt-get update", pty=True, hide=hide)

    cmd.cli.run(f"sudo apt-get install -y {pkgname}", pty=True, hide=hide)


def install(pkgname, version=None, update=True, hide=False) -> bool:
    """
    Установить пакет если он еще не установлен в системе

    :param pkgname: название пакета
    :param version: версия
    :param update: запустить apt-get update перед установкой
    :param hide: скрыть вывод этапов
    :return: `True` если пакет был установлен, `False` если пакет уже был установлен ранее
    """
    if is_pkg_installed(pkgname, version):
        if version:
            if not hide:
                log(f"{pkgname}={version} already installed")
        else:
            if not hide:
                log(f"{pkgname} already installed")
        return False
    force_install(pkgname=pkgname, version=version, update=update, hide=hide)
    return True


def install_multiple(*pkg_names: str, update=True, hide=False) -> bool:
    """
    Установить несколько пакетов, если они не установлены

    :param pkg_names: список пакетов которые нужно установить
    :param update: запустить apt-get update перед установкой
    :param hide: скрыть вывод этапов
    :return: `True` если хотя бы один пакет был установлен, `False` если все пакеты уже были установлен ранее
    """
    if all([is_pkg_installed(x) for x in pkg_names]):
        if not hide:
            log(f"{','.join(pkg_names)} already installed")
        return False

    if update:
        cmd.cli.run("sudo apt-get update", pty=True, hide=hide)

    for pkg in pkg_names:
        install(pkg, update=False, hide=hide)
    return True


def remove(*pkg_names: str, hide=False):
    """
    Удалить пакет

    :param pkg_names: список пакетов которые нужно удалить
    :param hide: скрыть вывод этапов
    """
    assert pkg_names, "pkg_names is empty"
    cmd.cli.run(f"sudo apt-get remove --auto-remove -y {' '.join(pkg_names)}", hide=hide)
