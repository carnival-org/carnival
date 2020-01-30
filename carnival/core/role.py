from typing import Type, TYPE_CHECKING, List, Dict, Any

from carnival import global_context
from carnival.host import Host
from carnival.core.utils import get_arg_names

if TYPE_CHECKING:
    from carnival.role import Role


def set_context(host: Host):
    global_context.conn = host.connect()
    global_context.host = host


def build_kwargs(fn, context: Dict[str, Any], secrets):
    arg_names: List[str] = get_arg_names(fn)
    kwargs = {}
    if 'secrets' in arg_names:
        kwargs['secrets'] = secrets

    for context_name, context_val in context.items():
        if context_name in arg_names:
            kwargs[context_name] = context_val
    return kwargs


class RoleExecutor:
    def __init__(self, role: Type['Role']):
        self.role = role

    def run(self, dry_run=False):
        for host in self.role.hosts:
            print(f"💃💃💃 Runing {self.role.name} at {host}")
            set_context(host)
            role = self.role()
            if not dry_run:
                kwargs = build_kwargs(role.run, host.context, global_context.secrets)
                role.run(**kwargs)
