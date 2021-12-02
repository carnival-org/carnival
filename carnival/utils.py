import typing
import os


def envvar(varname: str) -> str:
    """
    Получить переменную из окружения
    Замена context_ref для carnival v3
    :raises: ValueError если переменной в окружении нет
    """

    if varname not in os.environ:
        raise ValueError(f"{varname} is not persent in environment")

    return os.environ[varname]


def get_class_full_name(klass: typing.Type[typing.Any]) -> str:
    from carnival.cli import carnival_tasks_module

    klass_name = klass.__name__
    klass_mod = klass.__module__

    if klass_mod == "":
        return klass_name

    task_full_name = f"{klass_mod}.{klass_name}"

    if task_full_name.startswith(f"{carnival_tasks_module}."):
        task_full_name = task_full_name[len(carnival_tasks_module) + 1:]

    return task_full_name
