import os
import sys
import abc
from typing import Iterable, Type, Dict, Set

import click

from carnival.task import Task


def task_subclasses(cls) -> Set[Type]:
    # Get subclasses of task, which not abstract

    subclasses = set()
    for sc in cls.__subclasses__():
        # Skip if last MRO base is ABC
        if abc.ABC != sc.__mro__[1]:
            subclasses.add(sc)

        subclasses.update(task_subclasses(sc))

    return subclasses


def load_tasks_file(tasks_file: str) -> Dict[str, Type[Task]]:
    try:
        __import__(os.path.splitext(tasks_file)[0].replace("/", '.'))
    except ModuleNotFoundError:
        print(f"[WARN] {tasks_file} not exists", file=sys.stderr)
        return {}

    tasks: Dict[str, Type[Task]] = {}

    for task_class in task_subclasses(Task):
        tasks[task_class.get_name()] = task_class

    return tasks


def main():
    sys.path.insert(0, os.getcwd())
    carnival_file = os.getenv("CARNIVAL_FILE", "carnival_file.py")
    try:
        task_types = load_tasks_file(carnival_file)
    except FileNotFoundError:
        return 1

    @click.command()
    @click.option('-d', '--dry_run', is_flag=True, default=False, help="Simulate run")
    @click.argument('tasks', required=True, type=click.Choice(task_types.keys()), nargs=-1)
    def cli(dry_run: bool, tasks: Iterable[str]):
        for task in tasks:
            task_types[task](dry_run=dry_run).run()
    cli()
