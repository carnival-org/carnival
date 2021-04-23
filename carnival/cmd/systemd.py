from carnival import cmd
from invoke import Result  # type: ignore


def daemon_reload() -> Result:
    """
    Перегрузить systemd
    """
    return cmd.cli.run("sudo systemctl --system daemon-reload")


def start(service_name: str, reload_daemon: bool = False) -> Result:
    """
    Запустить сервис

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    """

    if reload_daemon:
        daemon_reload()
    return cmd.cli.run(f"sudo systemctl start {service_name}")


def stop(service_name: str, reload_daemon: bool = False) -> Result:
    """
    Остановить сервис

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    """
    if reload_daemon:
        daemon_reload()
    return cmd.cli.run(f"sudo systemctl stop {service_name}")


def restart(service_name: str) -> Result:
    """
    Перезапустить сервис

    :param service_name: имя сервиса
    """
    return cmd.cli.run(f"sudo systemctl restart {service_name}")


def enable(service_name: str, reload_daemon: bool = False, start_now: bool = True) -> Result:
    """
    Добавить сервис в автозапуск

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    :param start_now: запустить сервис после добавления
    """
    if reload_daemon:
        daemon_reload()

    res = cmd.cli.run(f"sudo systemctl enable {service_name}")

    if start_now:
        start(service_name)

    return res


def disable(service_name: str, reload_daemon: bool = False, stop_now: bool = True) -> Result:
    """
    Убрать сервис из автозапуска

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    :param stop_now: Остановить сервис
    """

    if reload_daemon:
        daemon_reload()

    res = cmd.cli.run(f"sudo systemctl disable {service_name}")

    if stop_now:
        stop(service_name)

    return res
