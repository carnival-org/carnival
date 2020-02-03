from carnival import cmd


def test_install_ce_ubuntu(suspend_capture, ubuntu_ssh_host_connection):
    with suspend_capture:
        assert cmd.fs.is_file_exists("/usr/bin/docker") is False
        cmd.docker.install_ce_ubuntu()
        assert cmd.fs.is_file_exists("/usr/bin/docker") is True
        cmd.apt.remove("docker-ce")


def test_install_compose(suspend_capture, ubuntu_ssh_host_connection):
    with suspend_capture:
        assert cmd.fs.is_file_exists("/usr/local/bin/docker-compose") is False
        cmd.docker.install_compose()
        assert cmd.fs.is_file_exists("/usr/local/bin/docker-compose") is True

        cmd.cli.run("rm /usr/local/bin/docker-compose")
