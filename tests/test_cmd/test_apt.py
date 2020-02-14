import pytest

from carnival import cmd, global_context


@pytest.mark.slow
def test_apt_install(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with global_context.SetContext(ubuntu_ssh_host):
            assert cmd.fs.is_file_exists("/usr/bin/mc") is False
            assert cmd.apt.install("mc", hide=True) is True
            assert cmd.apt.install("mc", hide=True) is False
            assert cmd.fs.is_file_exists("/usr/bin/mc") is True
            cmd.apt.remove("mc", hide=True)


@pytest.mark.slow
def test_apt_install_multiple(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with global_context.SetContext(ubuntu_ssh_host):
            assert cmd.fs.is_file_exists("/usr/bin/mc") is False
            assert cmd.fs.is_file_exists("/usr/bin/htop") is False
            assert cmd.apt.install_multiple("htop", "mc", hide=True) is True
            assert cmd.apt.install_multiple("htop", "mc", hide=True) is False
            assert cmd.fs.is_file_exists("/usr/bin/mc") is True
            assert cmd.fs.is_file_exists("/usr/bin/htop") is True
            cmd.apt.remove("mc", "htop", hide=True)


@pytest.mark.slow
def test_apt_get_installed_version(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with global_context.SetContext(ubuntu_ssh_host):
            assert cmd.fs.is_file_exists("/usr/bin/mc") is False
            assert cmd.apt.get_installed_version("mc") is None

            cmd.apt.install("mc", hide=True)

            assert cmd.fs.is_file_exists("/usr/bin/mc") is True
            ver = cmd.apt.get_installed_version("mc")
            assert ver in cmd.apt.get_pkg_versions("mc")
            assert isinstance(ver, str)
            assert " " not in ver
            cmd.apt.remove("mc", hide=True)


@pytest.mark.slow
def test_apt_is_pkg_installed(suspend_capture, ubuntu_ssh_host):
    with suspend_capture:
        with global_context.SetContext(ubuntu_ssh_host):
            assert cmd.fs.is_file_exists("/usr/bin/mc") is False
            assert cmd.apt.is_pkg_installed("mc") is False

            cmd.apt.install("mc", hide=True)

            assert cmd.fs.is_file_exists("/usr/bin/mc") is True
            assert cmd.apt.is_pkg_installed("mc") is True
            ver = cmd.apt.get_installed_version("mc")
            assert cmd.apt.is_pkg_installed("mc", ver) is True
            assert cmd.apt.is_pkg_installed("mc", "3i2oxyom3x3 ") is False
            cmd.apt.remove("mc", hide=True)
