from typing import List
import os

from carnival import cmd


def set_password(username: str, password: str):
    cmd.cli.pty(f"echo '{username}:{password}' | chpasswd", hide=True)


def ssh_authorized_keys_add(ssh_key: str, keys_file=".ssh/authorized_keys"):
    ssh_key = ssh_key.strip()

    cmd.cli.run("mkdir -p ~/.ssh")
    cmd.cli.run("chmod 700 ~/.ssh")
    cmd.cli.run(f"touch {keys_file}")

    if not cmd.fs.is_file_contains(keys_file, ssh_key, escape=True):
        cmd.cli.run(f"echo '{ssh_key}' >> {keys_file}")


def ssh_authorized_keys_list() -> List[str]:
    if cmd.fs.is_file_exists("~/.ssh/authorized_keys") is False:
        return []

    return cmd.cli.run("cat ~/.ssh/authorized_keys", hide=True).stdout.strip().split("\n")


def ssh_authorized_keys_ensure(*ssh_keys: str) -> None:
    for ssh_key in ssh_keys:
        ssh_authorized_keys_add(ssh_key)


def ssh_copy_id(pubkey_file="~/.ssh/id_rsa.pub") -> None:
    ssh_authorized_keys_add(open(os.path.expanduser(pubkey_file)).read().strip())


def get_current_user_name() -> str:
    return cmd.cli.run("id -u -n", hide=True).stdout.strip()


def get_current_user_id() -> int:
    return int(cmd.cli.run("id -u", hide=True).stdout.strip())


def is_current_user_root() -> bool:
    return get_current_user_id() == 0
