from jinja2 import Environment, DictLoader

from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_put_template(suspend_capture, host_context, mocker):
    with suspend_capture:
        mocker.patch(
            'carnival.templates.j2_env',
            new=Environment(loader=DictLoader({"index.html": "Hello: {{ name }}"})),
        )
        assert cmd.fs.is_file_exists("/index") is False
        cmd.transfer.put_template("index.html", "/index")
        assert cmd.fs.is_file_exists("/index") is True
        cmd.cli.run("rm /index")


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_rsync(suspend_capture, host_context, mocker):
    with suspend_capture:
        cmd.system.ssh_copy_id()
        assert cmd.fs.is_dir_exists("/docs") is False
        cmd.transfer.rsync("./docs", "/")
        assert cmd.fs.is_dir_exists("/docs") is True
        cmd.cli.run("rm -rf /docs")
