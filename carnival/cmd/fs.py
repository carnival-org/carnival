from patchwork import files  # type:ignore

from carnival import cmd

from carnival import global_context


def mkdirs(*dirs: str):
    return [cmd.cli.run(f"mkdir -p {x}", hide=True) for x in dirs]


def is_dir_exists(dir_path: str) -> bool:
    return cmd.cli.run(f"test -d {dir_path}", warn=True, hide=True).ok


def is_file_contains(filename, text, exact=False, escape=True) -> bool:
    # https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.contains
    return files.contains(global_context.conn, runner=global_context.conn.run, filename=filename, text=text, exact=exact, escape=escape)


def is_file_exists(path) -> bool:
    # https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.exists
    return files.exists(global_context.conn, runner=global_context.conn.run, path=path)


def ensure_dir_exists(path, user=None, group=None, mode=None) -> None:
    # https://fabric-patchwork.readthedocs.io/en/latest/api/files.html#patchwork.files.directory
    return files.directory(global_context.conn, runner=global_context.conn.run, path=path, user=user, group=group, mode=mode)
