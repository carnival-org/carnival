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


def get_task_full_name(carnival_tasks_module: str, task_class: Type[Task]) -> str:
    task_name = task_class.get_name()

    task_mod = task_class.__module__

    # Internal tasks always in root
    if task_mod.startswith("carnival."):
        return task_name

    task_full_name = f"{task_mod}.{task_name}"

    if task_mod.startswith(carnival_tasks_module):
        task_full_name = task_full_name[len(carnival_tasks_module) + 1:]

    return task_full_name


def load_tasks_file(carnival_tasks_module: str) -> Dict[str, Type[Task]]:
    try:
        __import__(carnival_tasks_module)
    except (ModuleNotFoundError, FileNotFoundError) as ex:
        print(f"Cannot import {carnival_tasks_module}: {ex}", file=sys.stderr)

    tasks: Dict[str, Type[Task]] = {}

    for task_class in task_subclasses(Task):
        tasks[get_task_full_name(carnival_tasks_module, task_class)] = task_class

    return tasks


def get_tasks() -> Dict[str, Type[Task]]:
    sys.path.insert(0, os.getcwd())
    from carnival import internal_tasks  # noqa
    carnival_tasks_module = os.getenv("CARNIVAL_TASKS_MODULE", "carnival_tasks")
    return load_tasks_file(carnival_tasks_module)


def main():
    task_types = get_tasks()

    @click.command()
    @click.option('-d', '--dry_run', is_flag=True, default=False, help="Simulate run")
    @click.argument('tasks', required=True, type=click.Choice(task_types.keys()), nargs=-1)
    def cli(dry_run: bool, tasks: Iterable[str]):
        for task in tasks:
            task_types[task](dry_run=dry_run).run()
    cli()
