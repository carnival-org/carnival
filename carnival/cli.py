import os
from typing import Iterable

import click
import dotenv

from carnival.tasks_loader import get_tasks

# Load dotenv first
carnival_dotenv = os.getenv("CARNIVAL_DOTENV", '.env')
try:
    dotenv.load_dotenv(dotenv_path=carnival_dotenv)
except OSError:
    # dotenv file not found
    pass

carnival_tasks_module = os.getenv("CARNIVAL_TASKS_MODULE", "carnival_tasks")


def is_completion_script(complete_var: str) -> bool:
    return os.getenv(complete_var, None) is not None


task_types: dict = {}


def main():
    global task_types

    complete_var = os.getenv("COMPLETE_VAR", "_CARNIVAL_COMPLETE")
    task_types = get_tasks(
        carnival_tasks_module=carnival_tasks_module,
        for_completion=is_completion_script(complete_var)
    )

    @click.command()
    @click.option('-d', '--dry_run', is_flag=True, default=False, help="Simulate run")
    @click.argument('tasks', required=True, type=click.Choice(task_types.keys()), nargs=-1)
    def cli(dry_run: bool, tasks: Iterable[str]):
        for task in tasks:
            task_types[task](dry_run=dry_run).run()

    cli(complete_var=complete_var)
