from jinja2 import Environment, DictLoader

from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd, global_context


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_put_template(suspend_capture, host, mocker):
    with suspend_capture:
        with global_context.SetContext(host):
            mocker.patch(
                'carnival.templates.j2_env',
                new=Environment(loader=DictLoader({"index.html": "Hello: {{ name }}"})),
            )
            assert cmd.fs.is_file_exists("/index") is False
            cmd.transfer.put_template("index.html", "/index")
            assert cmd.fs.is_file_exists("/index") is True
            cmd.cli.run("rm /index")


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_rsync(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            cmd.system.ssh_copy_id()
            assert cmd.fs.is_dir_exists("/docs") is False
            cmd.transfer.rsync("./docs", "/")
            assert cmd.fs.is_dir_exists("/docs") is True
            cmd.cli.run("rm -rf /docs")
