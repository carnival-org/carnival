from invoke import Result  # type: ignore

from carnival import global_context


def _run_command(command: str, **kwargs) -> Result:
    return global_context.conn.run(command, **kwargs)


def run(command: str, **kwargs) -> Result:
    return _run_command(command, **kwargs)


def pty(command: str, **kwargs) -> Result:
    return run(command, pty=True, **kwargs)
