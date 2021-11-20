import pytest
from carnival import cmd


@pytest.mark.slow
@pytest.mark.remote
def test_apt_install(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with ubuntu_ssh_host.connect() as c:
            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is False
            assert cmd.apt.install(c, "mc", hide=True) is True
            assert cmd.apt.install(c, "mc", hide=True) is False
            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is True
            cmd.apt.remove(c, "mc", hide=True)


@pytest.mark.slow
@pytest.mark.remote
def test_apt_install_multiple(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with ubuntu_ssh_host.connect() as c:
            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is False
            assert cmd.fs.is_file_exists(c, "/usr/bin/htop") is False
            assert cmd.apt.install_multiple(c, "htop", "mc", hide=True) is True
            assert cmd.apt.install_multiple(c, "htop", "mc", hide=True) is False
            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is True
            assert cmd.fs.is_file_exists(c, "/usr/bin/htop") is True
            cmd.apt.remove(c, "mc", "htop", hide=True)


@pytest.mark.slow
@pytest.mark.remote
def test_apt_get_installed_version(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with ubuntu_ssh_host.connect() as c:
            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is False
            assert cmd.apt.get_installed_version(c, "mc") is None

            cmd.apt.install(c, "mc", hide=True)

            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is True
            ver = cmd.apt.get_installed_version(c, "mc")
            assert ver in cmd.apt.get_pkg_versions(c, "mc")
            assert isinstance(ver, str)
            assert " " not in ver
            cmd.apt.remove(c, "mc", hide=True)


@pytest.mark.slow
@pytest.mark.remote
def test_apt_is_pkg_installed(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with ubuntu_ssh_host.connect() as c:
            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is False
            assert cmd.apt.is_pkg_installed(c, "mc") is False

            cmd.apt.install(c, "mc", hide=True)

            assert cmd.fs.is_file_exists(c, "/usr/bin/mc") is True
            assert cmd.apt.is_pkg_installed(c, "mc") is True
            ver = cmd.apt.get_installed_version(c, "mc")
            assert cmd.apt.is_pkg_installed(c, "mc", ver) is True
            assert cmd.apt.is_pkg_installed(c, "mc", "3i2oxyom3x3 ") is False
            cmd.apt.remove(c, "mc", hide=True)
