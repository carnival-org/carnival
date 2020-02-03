from carnival import global_context


def _run_command(command: str, **kwargs):
    return global_context.conn.run(command, **kwargs)


def run(command: str, **kwargs):
    return _run_command(command, **kwargs)


def pty(command: str, **kwargs):
    return run(command, pty=True, **kwargs)
