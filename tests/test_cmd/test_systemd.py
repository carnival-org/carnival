from carnival import cmd, global_context


def test_daemon_reload(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                cmd.systemd.daemon_reload()


def test_start(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                cmd.systemd.start("nginx", reload_daemon=True)


def test_stop(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                cmd.systemd.stop("nginx", reload_daemon=True)


def test_restart(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                cmd.systemd.restart("nginx")


def test_enable(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                cmd.systemd.enable("nginx", reload_daemon=True, start_now=True)


def test_disable(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                cmd.systemd.disable("nginx", reload_daemon=True, stop_now=True)
