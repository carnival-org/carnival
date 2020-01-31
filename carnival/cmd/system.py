from typing import List

from carnival import cmd


def set_password(username: str, password: str):
    raise NotImplementedError  # TODO


def ssh_append_id(ssh_key: str, keys_file=".ssh/authorized_keys"):
    ssh_key = ssh_key.strip()

    cmd.cli.run("mkdir -p ~/.ssh")
    cmd.cli.run("chmod 700 ~/.ssh")
    cmd.cli.run(f"touch {keys_file}")

    if not cmd.transfer.is_file_contains(keys_file, ssh_key, escape=True):
        cmd.cli.run(f"echo '{ssh_key}' >> {keys_file}")


def ssh_ensure_keys(ssh_keys: List[str]):
    for ssh_key in ssh_keys:
        ssh_append_id(ssh_key)
