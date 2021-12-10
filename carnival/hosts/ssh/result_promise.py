import typing

from paramiko.client import SSHClient

from carnival.hosts.base.result_promise import ResultPromise


class SshResultPromise(ResultPromise):
    def __init__(
        self,
        conn: SSHClient,
        command: str,
        cwd: typing.Optional[str],
        timeout: int,
        use_sudo: bool,
        env: typing.Optional[typing.Dict[str, str]] = None,
    ):
        self.timeout = timeout
        self.conn = conn

        if cwd is not None:
            command = f"cd {cwd}; {command}"

        if use_sudo is True:
            command = command.replace('"', '\\"')
            command = f'sudo -n -- sh -c "{command}"'

        self.command = command

        # https://stackoverflow.com/questions/39429680/python-paramiko-redirecting-stderr-is-affected-by-get-pty-true
        _, stdout, stderr = self.conn.exec_command(
            command,
            timeout=timeout,
            environment=env,
            get_pty=True,  # Combines stdout and stderr, we dont want it
        )
        self.stdout_channel = stdout.channel
        self.stdout = stdout  # type: ignore
        self.stderr = stderr  # type: ignore

    def is_done(self) -> bool:
        return self.stdout_channel.exit_status_ready()

    def wait(self) -> int:
        return self.stdout_channel.recv_exit_status()
