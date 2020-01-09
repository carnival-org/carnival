from itertools import chain
from typing import List, Any, Dict, Optional
from dataclasses import dataclass, field

from fabric import Connection
from carnival import context


@dataclass
class Host:
    addr: str
    context: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        return f"🖥 {self.addr}"

    def __hash__(self):
        return hash(self.addr)


class Inventory:
    def __init__(self):
        self.role_hosts: Dict[str, List[Host]] = {}

    def get_by_role(self, roles: Optional[List[str]]) -> List[Host]:
        res = []

        if roles is None:
            return list(chain(*self.role_hosts.values()))

        for role in roles:
            res += self.role_hosts.get(role, [])
        return list(set(res))

    @classmethod
    def set_context(cls, host: Host):
        context.conn = Connection(host.addr)
        context.host_context = host.context

    def host(self, role: str, addr: str, **host_context):
        h = Host(addr=addr, context=host_context)

        if role not in self.role_hosts:
            self.role_hosts[role] = []

        self.role_hosts[role].append(h)
