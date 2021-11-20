
import typing
import os
import subprocess
from invoke.context import Context  # type: ignore

from carnival.host.connection import Connection, Result


class _LocalConnection(Connection):
    def __init__(self) -> None:
        self.c = Context()

    def run(self, command: str, hide: bool = False, pty: bool = False) -> Result:
        return self.c.run(command, hide=hide, pty=pty)  # type: ignore

    def open_shell(self, shell_cmd: typing.Optional[str] = None, cwd: typing.Optional[str] = None) -> None:
        if shell_cmd is None:
            shell_cmd = os.getenv("SHELL", '/bin/sh')

        assert shell_cmd is not None
        proc = subprocess.Popen([shell_cmd, ], shell=True, cwd=cwd)
        proc.communicate()
