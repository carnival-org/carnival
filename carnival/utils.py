from carnival import context


def log(message: str):
    print(f"💃💃💃 {context.conn.host}> {message}")


def run_command(command: str, **kwargs):
    return context.conn.run(command, **kwargs)
