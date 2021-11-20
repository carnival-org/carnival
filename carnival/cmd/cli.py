from typing import Any

from carnival.host.connection import Connection, Result


def run(c: Connection, command: str, **kwargs: Any) -> Result:
    """
    Запустить комманду
    """
    return c.run(command, **kwargs)


def pty(c: Connection, command: str, hide: bool = False) -> Result:
    return c.run(command, pty=True, hide=hide)
