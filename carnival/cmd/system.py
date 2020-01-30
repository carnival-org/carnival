from typing import List

from carnival import cmd


def set_password(username: str, password: str):
    raise NotImplementedError  # TODO


def ssh_append_id(ssh_key: str):
    cmd.cli.run("mkdir -p ~/.ssh")
    cmd.cli.run("chmod 700 ~/.ssh")
    cmd.cli.run("touch ~/.ssh/authorized_keys")

    if not cmd.transfer.is_file_contains("~/.ssh/authorized_keys", ssh_key):
        cmd.cli.run(f"echo '{ssh_key}' >> ~/.ssh/authorized_keys")


def ssh_ensure_keys(ssh_keys: List[str]):
    for ssh_key in ssh_keys:
        ssh_append_id(ssh_key)
