from typing import List, Union

from carnival import Role
from carnival.core.role import RoleExecutor
from carnival.host import Host


class Task:
    name: str = ""

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def run(self, **kwargs):
        raise NotImplementedError

    def run_role(self, roles: Union[Role, List[Role]], hosts: Union[Host, List[Host]]):
        if not isinstance(roles, list) and not isinstance(roles, tuple):
            roles = [roles]

        if not isinstance(hosts, list) and not isinstance(hosts, tuple):
            hosts = [hosts]

        executor = RoleExecutor(roles, hosts=hosts)
        executor.run(dry_run=self.dry_run)
