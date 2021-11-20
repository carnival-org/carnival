import pytest
from carnival import cmd


@pytest.mark.remote
def test_daemon_reload(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                cmd.systemd.daemon_reload(c)


@pytest.mark.remote
def test_start(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                cmd.systemd.start(c, "nginx", reload_daemon=True)


@pytest.mark.remote
def test_stop(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                cmd.systemd.stop(c, "nginx", reload_daemon=True)


@pytest.mark.remote
def test_restart(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                cmd.systemd.restart(c, "nginx")


@pytest.mark.remote
def test_enable(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                cmd.systemd.enable(c, "nginx", reload_daemon=True, start_now=True)


@pytest.mark.remote
def test_disable(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with host.connect() as c:
                cmd.systemd.disable(c, "nginx", reload_daemon=True, stop_now=True)
