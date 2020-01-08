from typing import List, Any, Dict
from dataclasses import dataclass, field


@dataclass
class Host:
    addr: str
    context: Dict[str, Any] = field(default_factory=dict)


class Inventory:
    def __init__(self):
        self.role_hosts: Dict[str, List[Host]] = {}

    def get_by_role(self, role: str) -> List[Host]:
        hosts = self.role_hosts.get(role, [])
        return list(set(hosts))

    def host(self, role: str, addr: str, **context):
        h = Host(addr=addr, context=context)

        if role not in self.role_hosts:
            self.role_hosts[role] = []

        self.role_hosts[role].append(h)
