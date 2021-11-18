import pytest
from carnival import cmd
from jinja2 import DictLoader, Environment


@pytest.mark.remote
def test_put_template(suspend_capture, mocker, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                mocker.patch(
                    'carnival.templates.j2_env',
                    new=Environment(loader=DictLoader({"index.html": "Hello: {{ name }}"})),
                )
                assert cmd.transfer._is_path_exists(c, "/index") is False
                cmd.transfer.put_template(c, "index.html", "/index")
                assert cmd.transfer._is_path_exists(c, "/index") is True
                cmd.cli.run(c, "rm /index")


@pytest.mark.remote
def test_is_dir_exists(suspend_capture, local_host, ubuntu_ssh_host, centos_ssh_host):
    for host in [local_host, ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                assert cmd.transfer._is_path_exists(c, "/etc") is True
                assert cmd.transfer._is_path_exists(c, "/bin") is True
                assert cmd.transfer._is_path_exists(c, "/bin/sh") is True
                assert cmd.transfer._is_path_exists(c, "/bin/sh_noteist") is False
