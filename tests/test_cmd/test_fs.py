from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd, global_context


@parametrize_plus('host', [
    fixture_ref('local_host'),
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_is_dir_exists(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            assert cmd.fs.is_dir_exists("/etc")
            assert cmd.fs.is_dir_exists("/bin")


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_mkdirs(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            assert cmd.fs.is_dir_exists("/tmp/.carnivaltestdir1") is False
            assert cmd.fs.is_dir_exists("/tmp/.carnivaltestdir2") is False

            cmd.fs.mkdirs("/tmp/.carnivaltestdir1", "/tmp/.carnivaltestdir2")

            assert cmd.fs.is_dir_exists("/tmp/.carnivaltestdir1") is True
            assert cmd.fs.is_dir_exists("/tmp/.carnivaltestdir2") is True

            cmd.cli.run(f"rm -rf /tmp/.carnivaltestdir1 /tmp/.carnivaltestdir2")
