from typing import Any

from carnival import global_context
from invoke import Result  # type: ignore


def _run_command(command: str, **kwargs: Any) -> Result:
    assert global_context.conn is not None, "No connection"
    return global_context.conn.run(command, **kwargs)


def run(command: str, **kwargs: Any) -> Result:
    """
    Запустить комманду
    """
    return _run_command(command, **kwargs)


def pty(command: str, **kwargs: Any) -> Result:
    """
    Запустить комманду, используя псевдотерминальную сессию

    См <https://docs.pyinvoke.org/en/latest/api/runners.html>
    """
    return run(command, pty=True, **kwargs)
