import abc
import os
import sys
import typing
import collections

from carnival.task import TaskBase


def task_subclasses(cls: typing.Type[typing.Any]) -> typing.Set[typing.Type[typing.Any]]:
    # Get subclasses of task, which not abstract

    subclasses = set()
    for sc in cls.__subclasses__():
        # Skip if last MRO base is ABC
        if abc.ABC != sc.__mro__[1]:
            subclasses.add(sc)

        subclasses.update(task_subclasses(sc))

    return subclasses


def get_task_full_name(carnival_tasks_module: str, task_class: typing.Type[TaskBase]) -> str:
    task_name = task_class.get_name()

    task_mod = task_class.module_name
    if task_mod is None:
        task_mod = task_class.__module__

    if task_mod == "":
        return task_name

    task_full_name = f"{task_mod}.{task_name}"

    if task_full_name.startswith(f"{carnival_tasks_module}"):
        task_full_name = task_full_name[len(carnival_tasks_module) + 1:]

    return task_full_name


def import_tasks_file(carnival_tasks_module: str, silent: bool) -> None:
    try:
        __import__(carnival_tasks_module)
    except (ModuleNotFoundError, FileNotFoundError) as ex:
        if not silent:
            print(f"Cannot import {carnival_tasks_module}: {ex}", file=sys.stderr)


def get_tasks_from_runtime(carnival_tasks_module: str) -> typing.Dict[str, typing.Type["TaskBase"]]:
    from carnival.task import TaskBase

    tasks: typing.Dict[str, typing.Type["TaskBase"]] = {}

    for task_class in task_subclasses(TaskBase):
        task_full_name = get_task_full_name(carnival_tasks_module, task_class)
        tasks[task_full_name] = task_class

    return tasks


def get_tasks(
    carnival_tasks_module: str,
    for_completion: bool = False,
) -> typing.OrderedDict[str, typing.Type["TaskBase"]]:
    sys.path.insert(0, os.getcwd())
    from carnival import internal_tasks  # noqa
    import_tasks_file(carnival_tasks_module, silent=for_completion)
    return collections.OrderedDict(sorted(get_tasks_from_runtime(carnival_tasks_module).items()))
