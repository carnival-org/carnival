import os
import sys
import typing
import collections

import click
import dotenv

from carnival.task import TaskBase
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


task_types: typing.OrderedDict[str, typing.Type[TaskBase]] = collections.OrderedDict()


def except_hook(type: typing.Type[typing.Any], value: typing.Any, traceback: typing.Any) -> None:
    print(f"{type.__name__}: {value} \nYou can use --debug flag to see full traceback.")


def main() -> int:
    """
        >>> $ poetry run python -m carnival --help
        >>> Usage: python -m carnival [OPTIONS] {help|test}...
        >>> Options:
        >>> --debug        Turn on debug mode
        >>> --no_validate  Disable step validation
        >>> --help         Show this message and exit.
    """
    global task_types

    complete_var = os.getenv("COMPLETE_VAR", "_CARNIVAL_COMPLETE")
    task_types = get_tasks(
        carnival_tasks_module=carnival_tasks_module,
        for_completion=is_completion_script(complete_var)
    )

    @click.command()
    @click.option('--debug', is_flag=True, default=False, help="Turn on debug mode")
    @click.option('--no_validate', is_flag=True, default=False, help="Disable step validation")
    @click.argument('tasks', required=True, type=click.Choice(list(task_types.keys())), nargs=-1)
    def cli(debug: bool, no_validate: bool, tasks: typing.Iterable[str]) -> None:
        if debug is True:
            print("Debug mode on.")
        else:
            sys.excepthook = except_hook

        if no_validate:
            print("Step validation disabled")

        for task in tasks:
            task_types[task](no_validate=no_validate).run()

    cli(complete_var=complete_var)
    return 0
