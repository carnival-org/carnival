import os
import sys
import typing
import collections

import click

from carnival.task import TaskBase
from carnival.tasks_loader import get_tasks


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

        # Build chain and validate
        task_chain: typing.List[TaskBase] = []
        for task_class_str in tasks:
            task = task_types[task_class_str](no_validate=no_validate)
            if not task.no_validate:
                errors = task.validate()
                if errors:
                    print(f"There is validation errors for task {task_class_str}")
                    for e in errors:
                        print(f" * {e}")
                    return
            task_chain.append(task)

        # Run
        for task in task_chain:
            task.run()

    cli(complete_var=complete_var)
    return 0
