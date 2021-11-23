import pytest
from carnival import cmd, connection
from jinja2 import DictLoader, Environment


@pytest.mark.remote
def test_put_template(suspend_capture, mocker, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with connection.SetConnection(host):
                mocker.patch(
                    'carnival.templates.j2_env',
                    new=Environment(loader=DictLoader({"index.html": "Hello: {{ name }}"})),
                )
                assert cmd.fs.is_file_exists("/index") is False
                cmd.transfer.put_template("index.html", "/index")
                assert cmd.fs.is_file_exists("/index") is True
                cmd.cli.run("rm /index")


@pytest.mark.remote
def test_rsync(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with connection.SetConnection(host):
                cmd.system.ssh_copy_id()
                assert cmd.fs.is_dir_exists("/docs") is False
                cmd.transfer.rsync("./docs", "/", strict_host_keys=False)
                assert cmd.fs.is_dir_exists("/docs") is True
                cmd.cli.run("rm -rf /docs")
