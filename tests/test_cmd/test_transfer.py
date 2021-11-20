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
                assert cmd.fs.is_file_exists(c, "/index") is False
                cmd.transfer.put_template("index.html", c, "/index")
                assert cmd.fs.is_file_exists(c, "/index") is True
                cmd.cli.run(c, "rm /index")


# TODO: test_transfer
# TODO: test_getfo
# TODO: test_putfo
