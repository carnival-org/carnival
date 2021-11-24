import typing

from carnival import Connection, Result


def run(c: Connection, command: str, warn: bool = True, hide: bool = False, cwd: typing.Optional[str] = None) -> Result:
    """
    Запустить комманду

    См <https://docs.pyinvoke.org/en/latest/api/runners.html>
    """
    return c.run(command, warn=warn, hide=hide, cwd=cwd)


def is_cmd_exist(c: Connection, cmd_name: str) -> bool:
    return run(c, f"which {cmd_name}", hide=True, warn=True).ok
