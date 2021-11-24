import pytest
from carnival import cmd


@pytest.mark.remote
def test_run(suspend_capture, local_host, ubuntu_ssh_host, centos_ssh_host):
    for host in [local_host, ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                result = cmd.cli.run(c, "ls -1 /", hide=True)
                assert result.ok is True

                # Check response looks like root fs
                root_files = result.stdout.split("\n")
                assert 'bin' in root_files
                assert 'etc' in root_files
                assert 'usr' in root_files
                assert 'tmp' in root_files
                assert 'sbin' in root_files
