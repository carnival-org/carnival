import os
import sys
from typing import Iterable, Type, Dict, List

import click

from carnival.role import Role
from carnival.core.role import RoleExecutor
from carnival.core.utils import import_file, underscore


def load_roles_file(tasks_file: str) -> Dict[str, Type[Role]]:
    try:
        import_file(tasks_file)
    except ModuleNotFoundError:
        return {}

    roles: Dict[str, Type[Role]] = {}

    for r in Role.__subclasses__():
        if not r.name:
            r.name = underscore(r.__name__)
            assert r.name not in roles, f"Role {r.name} already defined"
            roles[r.name] = r

    return roles


def run_tasks(role: Iterable[str], dry_run: bool, roles: Dict[str, Type[Role]], hosts: List[str]):
    for r in role:
        executor = RoleExecutor(roles[r], hosts=hosts)
        executor.run(dry_run=dry_run)


def main():
    sys.path.insert(0, os.getcwd())
    carnival_file = os.getenv("CARNIVAL_FILE", "carnival_file.py")
    try:
        roles = load_roles_file(carnival_file)
    except FileNotFoundError:
        print(f"Carnival file ({carnival_file}) not found.")
        return

    @click.command()
    @click.option('-d', '--dry_run', is_flag=True, default=False, help="Simulate run")
    @click.option('-H', '--host', multiple=True, help="Filter hosts on each role")
    @click.argument('role', required=True, type=click.Choice(roles.keys()), nargs=-1)
    def cli(dry_run: bool, role: Iterable[str], host: List[str]):
        run_tasks(role=role, dry_run=dry_run, roles=roles, hosts=host)
    cli()
