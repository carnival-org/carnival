import importlib.util
import re
import os
from typing import Iterable, Type, Dict

import click

from carnival.role import Role, RoleExecutor


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def import_file(module_path: str):
    spec = importlib.util.spec_from_file_location(f"carnival.__{module_path}", module_path)
    _module = importlib.util.module_from_spec(spec)
    return spec.loader.exec_module(_module)


def load_roles_file(tasks_file: str) -> Dict[str, Type[Role]]:
    import_file(tasks_file)
    roles: Dict[str, Type[Role]] = {}

    for r in Role.__subclasses__():
        if not r.name:
            r.name = _underscore(r.__name__)
            assert r.name not in roles, f"Role {r.name} already defined"
            roles[r.name] = r

    return roles


def run_tasks(role: Iterable[str], dry_run: bool, roles: Dict[str, Type[Role]]):
    for r in role:
        executor = RoleExecutor(roles[r])
        executor.run(dry_run=dry_run)


def main():
    carnival_file = os.getenv("CARNIVAL_FILE", "carnival_file.py")
    try:
        roles = load_roles_file(carnival_file)
    except FileNotFoundError:
        print(f"Carnival file ({carnival_file}) not found.")
        return

    @click.command()
    @click.option('-d', '--dry_run', is_flag=True, default=False)
    @click.argument('role', required=True, type=click.Choice(roles.keys()), nargs=-1)
    def cli(dry_run: bool, role: Iterable[str]):
        run_tasks(role=role, dry_run=dry_run, roles=roles)

    cli()
