import pytest
from carnival import cmd


@pytest.mark.remote
def test_get_current_user_name(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                assert cmd.system.get_current_user_name(c) == 'root'


@pytest.mark.remote
def test_get_current_user_id(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                assert cmd.system.get_current_user_id(c) == 0


@pytest.mark.remote
def test_is_current_user_root(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                assert cmd.system.is_current_user_root(c) is True
