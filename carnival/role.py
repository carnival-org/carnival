from typing import List

from carnival.host import Host


class Role:
    name: str = ""
    hosts: List[Host] = []

    def run(self):
        raise NotImplementedError
