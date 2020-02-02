from carnival import cmd


def test_apt(suspend_capture, ubuntu_ssh_host_connection):
    with suspend_capture:
        assert cmd.transfer.is_file_exists("/usr/bin/mc") is False
        cmd.apt.install("mc", hide=True)
        assert cmd.transfer.is_file_exists("/usr/bin/mc") is True
        cmd.apt.remove("mc", hide=True)

        assert cmd.transfer.is_file_exists("/usr/bin/mc") is False
        assert cmd.transfer.is_file_exists("/usr/bin/htop") is False
        cmd.apt.install_multiple("htop", "mc", hide=True)
        assert cmd.transfer.is_file_exists("/usr/bin/mc") is True
        assert cmd.transfer.is_file_exists("/usr/bin/htop") is True
