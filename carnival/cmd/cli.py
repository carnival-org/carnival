from typing import Any

from carnival.connection import AnyConnection, Result


def run(c: AnyConnection, command: str, **kwargs: Any) -> Result:
    """
    Запустить комманду
    """
    return c.run(command, **kwargs)


def pty(c: AnyConnection, command: str, hide: bool = False) -> Result:
    return c.run(command, pty=True, hide=hide)
