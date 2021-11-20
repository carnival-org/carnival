from carnival import cmd
from carnival.host.connection import Result, Connection


def daemon_reload(c: Connection) -> Result:
    """
    Перегрузить systemd
    """
    return cmd.cli.run(c, "sudo systemctl --system daemon-reload")


def start(c: Connection, service_name: str, reload_daemon: bool = False) -> Result:
    """
    Запустить сервис

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    """

    if reload_daemon:
        daemon_reload(c)
    return cmd.cli.run(c, f"sudo systemctl start {service_name}")


def stop(c: Connection, service_name: str, reload_daemon: bool = False) -> Result:
    """
    Остановить сервис

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    """
    if reload_daemon:
        daemon_reload(c)
    return cmd.cli.run(c, f"sudo systemctl stop {service_name}")


def restart(c: Connection, service_name: str) -> Result:
    """
    Перезапустить сервис

    :param service_name: имя сервиса
    """
    return cmd.cli.run(c, f"sudo systemctl restart {service_name}")


def enable(c: Connection, service_name: str, reload_daemon: bool = False, start_now: bool = True) -> Result:
    """
    Добавить сервис в автозапуск

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    :param start_now: запустить сервис после добавления
    """
    if reload_daemon:
        daemon_reload(c)

    res = cmd.cli.run(c, f"sudo systemctl enable {service_name}")

    if start_now:
        start(c, service_name)

    return res


def disable(c: Connection, service_name: str, reload_daemon: bool = False, stop_now: bool = True) -> Result:
    """
    Убрать сервис из автозапуска

    :param service_name: имя сервиса
    :param reload_daemon: перегрузить systemd
    :param stop_now: Остановить сервис
    """

    if reload_daemon:
        daemon_reload(c)

    res = cmd.cli.run(c, f"sudo systemctl disable {service_name}")

    if stop_now:
        stop(c, service_name)

    return res
