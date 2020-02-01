from typing import List, Union

import re

from carnival import global_context, Step

from carnival.host import Host


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


class Task:
    name: str = ""

    @classmethod
    def get_name(cls) -> str:
        return cls.name if cls.name else _underscore(cls.__name__)

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def step(self, roles: Union[Step, List[Step]], hosts: Union[Host, List[Host]]):
        if not isinstance(roles, list) and not isinstance(roles, tuple):
            roles = [roles, ]

        if not isinstance(hosts, list) and not isinstance(hosts, tuple):
            hosts = [hosts, ]

        for host in hosts:
            global_context.set_context(host)

            for role in roles:
                role_name = _underscore(role.__class__.__name__)
                print(f"💃💃💃 Running {role_name} at {host}")
                if not self.dry_run:
                    role.run_with_context(host=host)

    def run(self, **kwargs):
        raise NotImplementedError
