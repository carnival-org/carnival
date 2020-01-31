from typing import Type, TYPE_CHECKING, List, Dict, Any

from carnival.host import Host

from carnival import global_context
from carnival.core.utils import get_arg_names
from carnival.secrets_manager import secrets_storage

if TYPE_CHECKING:
    from carnival.role import Role


def build_kwargs(fn, context: Dict[str, Any], secrets, host: Host):
    arg_names: List[str] = get_arg_names(fn)
    kwargs = {}
    if 'secrets' in arg_names:
        kwargs['secrets'] = secrets

    if 'host' in arg_names:
        kwargs['host'] = host

    for context_name, context_val in context.items():
        if context_name in arg_names:
            kwargs[context_name] = context_val
    return kwargs


class RoleExecutor:
    def __init__(self, role: Type['Role'], hosts: List[str]):
        self.role = role
        self.hosts = hosts

    def run(self, dry_run=False):
        for host in self.role.hosts:
            if self.hosts and host.addr not in self.hosts:
                print(f"💃💃💃 Skipping {self.role.name} at {host}")
                continue
            print(f"💃💃💃 Running {self.role.name} at {host}")
            global_context.set_context(host)
            role = self.role()
            if not dry_run:
                kwargs = build_kwargs(role.run, context=host.context, secrets=secrets_storage, host=host)
                role.run(**kwargs)
