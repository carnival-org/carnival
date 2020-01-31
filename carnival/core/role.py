from typing import List, Dict, Any

from carnival.host import Host

from carnival import global_context, Role
from carnival.core.utils import get_arg_names
from carnival.secrets_manager import secrets_storage


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
    def __init__(self, roles: List[Role], hosts: List[Host]):
        self.roles = roles
        self.hosts = hosts

    def run(self, dry_run=False):
        for host in self.hosts:
            global_context.set_context(host)

            for role in self.roles:
                name = role.name if role.name else role.__class__.__name__
                print(f"💃💃💃 Running {name} at {host}")
                if not dry_run:
                    kwargs = build_kwargs(role.run, context=host.context, secrets=secrets_storage, host=host)
                    role.run(**kwargs)
