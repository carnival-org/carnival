from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
])
def test_install_ce_ubuntu(suspend_capture, host_context):
    with suspend_capture:
        assert cmd.fs.is_file_exists("/usr/bin/docker") is False
        cmd.docker.install_ce_ubuntu()
        assert cmd.fs.is_file_exists("/usr/bin/docker") is True
        cmd.apt.remove("docker-ce")


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_install_compose(suspend_capture, host_context):
    with suspend_capture:
        assert cmd.fs.is_file_exists("/usr/local/bin/docker-compose") is False
        cmd.docker.install_compose()
        assert cmd.fs.is_file_exists("/usr/local/bin/docker-compose") is True

        cmd.cli.run("rm /usr/local/bin/docker-compose")
