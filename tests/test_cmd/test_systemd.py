from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_daemon_reload(suspend_capture, host_context):
    with suspend_capture:
        cmd.systemd.daemon_reload()


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_start(suspend_capture, host_context):
    with suspend_capture:
        cmd.systemd.start("nginx", reload_daemon=True)


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_stop(suspend_capture, host_context):
    with suspend_capture:
        cmd.systemd.stop("nginx", reload_daemon=True)


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_restart(suspend_capture, host_context):
    with suspend_capture:
        cmd.systemd.restart("nginx")


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_enable(suspend_capture, host_context):
    with suspend_capture:
        cmd.systemd.enable("nginx", reload_daemon=True, start_now=True)


@parametrize_plus('host_context', [
    fixture_ref('ubuntu_ssh_host_connection'),
    fixture_ref('centos_ssh_host_connection'),
])
def test_disable(suspend_capture, host_context):
    with suspend_capture:
        cmd.systemd.disable("nginx", reload_daemon=True, stop_now=True)
