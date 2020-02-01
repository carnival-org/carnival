from carnival import cmd


def daemon_reload():
    cmd.cli.run(f"sudo systemctl --system daemon-reload")


def start(service_name: str, reload_daemon=False):
    if reload_daemon:
        daemon_reload()
    cmd.cli.run(f"sudo systemctl start {service_name}")


def stop(service_name: str, reload_daemon=False):
    if reload_daemon:
        daemon_reload()
    cmd.cli.run(f"sudo systemctl stop {service_name}")


def restart(service_name: str):
    cmd.cli.run(f"sudo systemctl restart {service_name}")


def enable(service_name: str, reload_daemon=False, start_now=True):
    if reload_daemon:
        daemon_reload()
    cmd.cli.run(f"sudo systemctl enable {service_name}")
    if start_now:
        start(service_name)


def disable(service_name: str, reload_daemon=False, stop_now=True):
    if reload_daemon:
        daemon_reload()
    cmd.cli.run(f"sudo systemctl disable {service_name}")
    if stop_now:
        stop(service_name)
