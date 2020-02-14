import pytest
from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd, global_context


@pytest.mark.slow
@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
])
def test_install_ce_ubuntu(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            assert cmd.fs.is_file_exists("/usr/bin/docker") is False
            cmd.docker.install_ce_ubuntu()
            assert cmd.fs.is_file_exists("/usr/bin/docker") is True
            cmd.apt.remove("docker-ce")


@pytest.mark.slow
@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_install_compose(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            assert cmd.fs.is_file_exists("/usr/local/bin/docker-compose") is False
            cmd.docker.install_compose()
            assert cmd.fs.is_file_exists("/usr/local/bin/docker-compose") is True

            cmd.cli.run("rm /usr/local/bin/docker-compose")
