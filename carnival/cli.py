import os
import sys
from typing import Iterable, Type, Dict

import click

from carnival.core.utils import import_file, underscore
from carnival.task import Task


def load_tasks_file(tasks_file: str) -> Dict[str, Type[Task]]:
    try:
        import_file(tasks_file)
    except ModuleNotFoundError:
        return {}

    tasks: Dict[str, Type[Task]] = {}

    for t in Task.__subclasses__():
        if not t.name:
            t.name = underscore(t.__name__)
            assert t.name not in tasks, f"Task {t.name} already defined"
            tasks[t.name] = t

    return tasks


def run_tasks(tasks: Iterable[str], dry_run: bool, task_types: Dict[str, Type[Task]]):
    for p in tasks:
        task_types[p](
            dry_run=dry_run
        ).run()


def main():
    sys.path.insert(0, os.getcwd())
    carnival_file = os.getenv("CARNIVAL_FILE", "carnival_file.py")
    try:
        task_types = load_tasks_file(carnival_file)
    except FileNotFoundError:
        print(f"Carnival file ({carnival_file}) not found.")
        return

    @click.command()
    @click.option('-d', '--dry_run', is_flag=True, default=False, help="Simulate run")
    @click.argument('tasks', required=True, type=click.Choice(task_types.keys()), nargs=-1)
    def cli(dry_run: bool, tasks: Iterable[str]):
        run_tasks(tasks=tasks, dry_run=dry_run, task_types=task_types)
    cli()
