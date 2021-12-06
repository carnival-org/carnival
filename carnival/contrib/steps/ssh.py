import os
import re

from carnival import Step
from carnival import Connection


def _escape_for_regex(text: str) -> str:
    """
    Tnx to https://stackoverflow.com/questions/280435/escaping-regex-string
    :param text:
    :return:
    """
    regex = re.escape(text)
    # double escaping for \
    regex = regex.replace("\\\\", "\\\\\\")
    # triple-escaping for $ signs
    regex = regex.replace(r"\$", r"\\\$")
    # single quotes should not be escaped
    regex = regex.replace(r"\'", "'")
    return regex


def _is_file_contains(c: Connection, filename: str, text: str, escape: bool = True) -> bool:
    """
    Содержит ли файл текст

    :param c: Конект с хостом
    :param filename: путь до файла
    :param text: текст который нужно искать
    :param escape: экранировать ли текст
    """
    if escape:
        text = _escape_for_regex(text)
    egrep_cmd = 'egrep "{}" "{}"'.format(text, filename)
    return c.run(egrep_cmd, hide=True, warn=True).ok


class AddAuthorizedKey(Step):
    """
    Добавить ssh ключ в `authorized_keys` если его там нет
    """

    def __init__(self, ssh_key: str, keys_file: str = ".ssh/authorized_keys") -> None:
        """
        :param ssh_key: ключ
        :param keys_file: пусть до файла `authorized_keys`
        :return: `True` если ключ был добавлен, `False` если ключ уже был в файле
        """
        self.ssh_key = ssh_key.strip()
        self.keys_file = keys_file

    def run(self, c: Connection) -> bool:
        c.run("mkdir -p ~/.ssh")
        c.run("chmod 700 ~/.ssh")
        c.run(f"touch {self.keys_file}")

        if not _is_file_contains(c, self.keys_file, self.ssh_key, escape=True):
            c.run(f"echo '{self.ssh_key}' >> {self.keys_file}")
            return True
        return False


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

    def run(self, c: Connection) -> bool:
        key = open(os.path.expanduser(self.pubkey_file)).read().strip()
        return AddAuthorizedKey(key).run(c=c)
