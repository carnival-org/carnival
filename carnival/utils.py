from carnival import global_context


def log(message: str, file=None):
    print(f"💃💃💃 {global_context.conn.host}> {message}", file=file)
