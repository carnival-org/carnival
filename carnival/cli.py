import os
import sys
from typing import Iterable, Type, Dict

import click

from carnival.task import Task


def load_tasks_file(tasks_file: str) -> Dict[str, Type[Task]]:
    try:
        __import__(os.path.splitext(tasks_file)[0])
    except ModuleNotFoundError:
        return {}

    tasks: Dict[str, Type[Task]] = {}

    for task_class in Task.__subclasses__():
        tasks[task_class.get_name()] = task_class

    return tasks


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
        for task in tasks:
            task_types[task](dry_run=dry_run).run()
    cli()
