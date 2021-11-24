import typing

from carnival import Connection, Result


def run(c: Connection, command: str, warn: bool = True, hide: bool = False, cwd: typing.Optional[str] = None) -> Result:
    """
    Запустить команду

    :param c: Конект с хостом
    :param command: Команда для запуска
    :param warn: Вывести stderr
    :param hide: Скрыть вывод команды
    :param cwd: Перейти в папку при выполнении команды
    """
    return c.run(command, warn=warn, hide=hide, cwd=cwd)


def is_cmd_exist(c: Connection, cmd_name: str) -> bool:
    """
    Проверить есть ли команда в $PATH

    :param c: Конект с хостом
    :param command: Команда
    """
    return run(c, f"which {cmd_name}", hide=True, warn=True).ok
