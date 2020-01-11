from carnival import global_context


def log(message: str, file=None):
    print(f"💃💃💃 {global_context.conn.host}> {message}", file=file)


def run_command(command: str, **kwargs):
    return global_context.conn.run(command, **kwargs)
