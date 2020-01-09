from typing import Optional

import invoke

from carnival import cmd
from carnival.utils import log


def get_installed_version(pkgname: str) -> Optional[str]:
    """
    Get installed package version
    Returns None if package not installed
    """
    try:
        ver = cmd.cli.run(f"dpkg -s {pkgname} | grep Version", hide='both').stdout
    except invoke.exceptions.UnexpectedExit as ex:
        stderr = ex.result.tail("stderr")
        if 'is not installed and no information is available' in stderr:
            return None
        raise ValueError from ex

    _, v = ver.split("Version: ")
    return v.strip()


def is_pkg_installed(pkgname: str, version=None) -> bool:
    """
    Check is package installed?
    If version not specified - check any version
    """

    pkgver = get_installed_version(pkgname)
    if version is None and pkgver is not None:
        return True

    if version is not None and pkgver == version:
        return True

    return False


def force_install(pkgname, version=None, update=False):
    """
    Install apt package
    """
    if version:
        pkgname = f"{pkgname}={version}"

    if update:
        cmd.cli.run("sudo apt-get update", pty=True)

    cmd.cli.run(f"sudo apt-get install -y {pkgname}", pty=True)


def install(pkgname, version=None, update=True) -> bool:
    """
    Install apt package if not installed
    Returns true if installed, false if was already installed
    """
    if is_pkg_installed(pkgname, version):
        if version:
            log(f"{pkgname}={version} already installed")
        else:
            log(f"{pkgname} already installed")
        return False
    force_install(pkgname=pkgname, version=version, update=update)
    return True


def install_multiple(*pkg_names: str, update=True):
    if all([is_pkg_installed(x) for x in pkg_names]):
        log(f"{','.join(pkg_names)} already installed")
        return False

    if update:
        cmd.cli.run("sudo apt-get update", pty=True)

    for pkg in pkg_names:
        install(pkg, update=False)
    return True
