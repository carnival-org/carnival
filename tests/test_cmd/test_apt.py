from carnival import cmd


def test_apt_install(suspend_capture, ubuntu_ssh_host_connection):
    with suspend_capture:
        assert cmd.transfer.is_file_exists("/usr/bin/mc") is False
        cmd.apt.install("mc", hide=True)
        assert cmd.transfer.is_file_exists("/usr/bin/mc") is True
        cmd.apt.remove("mc", hide=True)


def test_apt_install_multiple(suspend_capture, ubuntu_ssh_host_connection):
    with suspend_capture:
        assert cmd.transfer.is_file_exists("/usr/bin/mc") is False
        assert cmd.transfer.is_file_exists("/usr/bin/htop") is False
        cmd.apt.install_multiple("htop", "mc", hide=True)
        assert cmd.transfer.is_file_exists("/usr/bin/mc") is True
        assert cmd.transfer.is_file_exists("/usr/bin/htop") is True
        cmd.apt.remove("mc", "htop", hide=True)


def test_apt_get_installed_version(suspend_capture, ubuntu_ssh_host_connection):
    with suspend_capture:
        with suspend_capture:
            assert cmd.transfer.is_file_exists("/usr/bin/mc") is False
            assert cmd.apt.get_installed_version("mc") is None

            cmd.apt.install("mc", hide=True)

            assert cmd.transfer.is_file_exists("/usr/bin/mc") is True
            ver = cmd.apt.get_installed_version("mc")
            assert isinstance(ver, str)
            assert " " not in ver
            cmd.apt.remove("mc", hide=True)


def test_apt_is_pkg_installed(suspend_capture, ubuntu_ssh_host_connection):
    with suspend_capture:
        with suspend_capture:
            assert cmd.transfer.is_file_exists("/usr/bin/mc") is False
            assert cmd.apt.is_pkg_installed("mc") is False

            cmd.apt.install("mc", hide=True)

            assert cmd.transfer.is_file_exists("/usr/bin/mc") is True
            assert cmd.apt.is_pkg_installed("mc") is True
            ver = cmd.apt.get_installed_version("mc")
            assert cmd.apt.is_pkg_installed("mc", ver) is True
            assert cmd.apt.is_pkg_installed("mc", "3i2oxyom3x3 ") is False
            cmd.apt.remove("mc", hide=True)
