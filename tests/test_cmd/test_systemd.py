from pytest_cases import fixture_ref, parametrize_plus

from carnival import cmd, global_context


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_daemon_reload(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            cmd.systemd.daemon_reload()


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_start(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            cmd.systemd.start("nginx", reload_daemon=True)


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_stop(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            cmd.systemd.stop("nginx", reload_daemon=True)


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_restart(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            cmd.systemd.restart("nginx")


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_enable(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            cmd.systemd.enable("nginx", reload_daemon=True, start_now=True)


@parametrize_plus('host', [
    fixture_ref('ubuntu_ssh_host'),
    fixture_ref('centos_ssh_host'),
])
def test_disable(suspend_capture, host):
    with suspend_capture:
        with global_context.SetContext(host):
            cmd.systemd.disable("nginx", reload_daemon=True, stop_now=True)
