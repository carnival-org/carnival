from carnival.context import conn


def log(message: str):
    print(f"{conn.host}> {message}")


def run_command(command: str, **kwargs):
    return conn.run(command, **kwargs)
