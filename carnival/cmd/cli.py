from carnival.host.connection import Connection, Result


def run(c: Connection, command: str, hide: bool = False, warn: bool = True) -> Result:
    """
    Запустить комманду
    """
    return c.run(command, hide=hide, warn=warn)


def is_cmd_exist(c: Connection, cmd_name: str) -> bool:
    return run(c, f"which -s {cmd_name}", hide=True, warn=True).ok
