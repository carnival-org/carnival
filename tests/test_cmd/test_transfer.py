from jinja2 import Environment, DictLoader

from carnival import cmd, global_context


def test_put_template(suspend_capture, mocker, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
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


def test_rsync(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                cmd.system.ssh_copy_id()
                assert cmd.fs.is_dir_exists("/docs") is False
                cmd.transfer.rsync("./docs", "/")
                assert cmd.fs.is_dir_exists("/docs") is True
                cmd.cli.run("rm -rf /docs")
