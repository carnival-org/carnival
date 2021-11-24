from carnival.host import AnyConnection
from invoke import Result  # type: ignore


def run(c: AnyConnection, command: str, warn: bool = True, hide: bool = False) -> Result:
    """
    Запустить комманду

    См <https://docs.pyinvoke.org/en/latest/api/runners.html>
    """
    return c.run(command, pty=True, warn=warn, hide=hide)
