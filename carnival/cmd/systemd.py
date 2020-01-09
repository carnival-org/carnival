from carnival import cmd


def start(service_name: str, daemon_reload=False):
    if daemon_reload:
        cmd.cli.run(f"sudo systemctl --system daemon-reload")
    cmd.cli.run(f"sudo systemctl start {service_name}")


def stop(service_name: str, daemon_reload=False):
    if daemon_reload:
        cmd.cli.run(f"sudo systemctl --system daemon-reload")
    cmd.cli.run(f"sudo systemctl stop {service_name}")


def enable(service_name: str, daemon_reload=False, start_now=True):
    if daemon_reload:
        cmd.cli.run(f"sudo systemctl --system daemon-reload")
    cmd.cli.run(f"sudo systemctl enable {service_name}")
    if start_now:
        start(service_name)


def disable(service_name: str, daemon_reload=False, stop_now=True):
    if daemon_reload:
        cmd.cli.run(f"sudo systemctl --system daemon-reload")
    cmd.cli.run(f"sudo systemctl disable {service_name}")
    if stop_now:
        stop(service_name)
