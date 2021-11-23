from typing import Any

from carnival import connection
from invoke import Result  # type: ignore


def _run_command(command: str, **kwargs: Any) -> Result:
    assert connection.conn is not None, "No connection"
    return connection.conn.run(command, **kwargs)


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
