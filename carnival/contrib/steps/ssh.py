import os

from carnival.steps import Step, shortcuts
from carnival import Connection


class AddAuthorizedKey(Step):
    """
    Добавить ssh ключ в `authorized_keys` если его там нет
    """

    def __init__(self, ssh_key: str) -> None:
        """
        :param ssh_key: ключ
        :param keys_file: пусть до файла `authorized_keys`
        :return: `True` если ключ был добавлен, `False` если ключ уже был в файле
        """
        self.ssh_key = ssh_key.strip()
        self.keys_file: str = "~/.ssh/authorized_keys"

    def run(self, c: Connection) -> None:
        c.run("mkdir -p ~/.ssh", use_sudo=False)
        c.run("chmod 700 ~/.ssh", use_sudo=False)
        c.run(f"touch {self.keys_file}", use_sudo=False)

        if not shortcuts.is_file_contains(c, self.keys_file, self.ssh_key, escape=True):
            shortcuts.append_string_to_file(c, file=self.keys_file, string=self.ssh_key)
            self.log_action("ssh key", "added")


class CopyId(Step):
    """
    Добавить публичный ssh-ключ текущего пользователя в авторизованные
    """

    def __init__(self, pubkey_file: str = "~/.ssh/id_rsa.pub") -> None:
        """
        :param pubkey_file: путь до файла с публичным ключем
        :return: `True` если ключ был добавлен, `False` если ключ уже был в файле
        """
        self.pubkey_file = pubkey_file

    def run(self, c: Connection) -> None:
        with open(os.path.expanduser(self.pubkey_file)) as fp:
            key = fp.read().strip()
        AddAuthorizedKey(key).run(c=c)
