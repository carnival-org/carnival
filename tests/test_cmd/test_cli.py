from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd


@parametrize_plus('host_context', [
    fixture_ref('local_host_connection_context'),
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_run(suspend_capture, host_context):
    with suspend_capture:
        result = cmd.cli.run("ls -1 /", hide=True)
        assert result.ok is True

        # Check response looks like root fs
        root_files = result.stdout.split("\n")
        assert 'bin' in root_files
        assert 'etc' in root_files
        assert 'usr' in root_files
        assert 'tmp' in root_files
        assert 'sbin' in root_files


@parametrize_plus('host_context', [
    fixture_ref('local_host_connection_context'),
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_pty(suspend_capture, host_context):
    with suspend_capture:
        result = cmd.cli.pty("ls -1 / | grep bin", hide=True)
        assert result.ok is True

        # Check response looks like root fs, filtered 'bin'
        root_files = result.stdout.split("\n")
        assert 'bin\r' in root_files
        assert 'sbin\r' in root_files
