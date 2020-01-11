from typing import List, Type

from carnival import global_context

from carnival.host import Host


def set_context(host: Host):
    global_context.conn = host.connect()
    global_context.host = host
    global_context.context = host.context


class Role:
    name: str = ""
    hosts: List[Host] = []

    def run(self):
        raise NotImplementedError


class RoleExecutor:
    def __init__(self, role: Type[Role]):
        self.role = role

    def run(self, dry_run=False):
        for host in self.role.hosts:
            print(f"💃💃💃 Runing {self.role.name} at {host}")
            set_context(host)
            role = self.role()
            if not dry_run:
                role.run()
