from invoke import Result  # type: ignore

from carnival import global_context


def _run_command(command: str, **kwargs) -> Result:
    return global_context.conn.run(command, **kwargs)


def run(command: str, **kwargs) -> Result:
    """
    Запустить комманду
    """
    return _run_command(command, **kwargs)


def pty(command: str, **kwargs) -> Result:
    """
    Запустить комманду, используя псевдотерминальную сессию

    См <https://docs.pyinvoke.org/en/latest/api/runners.html>
    """
    return run(command, pty=True, **kwargs)
