import typing
import os
from subprocess import Popen, PIPE

from carnival.hosts.base.result_promise import ResultPromise
from carnival.hosts.base.result import Result


class LocalResultPromise(ResultPromise):
    def __init__(
        self,
        command: str,
        timeout: int,
        cwd: typing.Optional[str],
        use_sudo: bool,
        env: typing.Optional[typing.Dict[str, str]] = None,
    ):
        proc_env = os.environ.copy()
        if env is not None:
            proc_env.update(env)

        if use_sudo is True:
            command = f"sudo -n -- sh -c '{command}'"

        self.proc = Popen(
            command, shell=True,
            stderr=PIPE, stdin=PIPE, stdout=PIPE, cwd=cwd,
            env=proc_env,
        )
        self.command = command
        assert self.proc.stdout is not None
        assert self.proc.stderr is not None
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        self.timeout = timeout

    def is_done(self) -> bool:
        return self.proc.poll() is not None

    def wait(self) -> int:
        return self.proc.wait(timeout=self.timeout)

    def get_result(self, hide: bool, show_command: bool = False) -> Result:
        result = super().get_result(hide=hide, show_command=show_command)
        self.proc.__exit__(None, None, None)
        return result
