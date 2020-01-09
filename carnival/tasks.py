from typing import List, Optional

from carnival.context import tasks
from carnival.core.tasks import Task


def task(
        roles: Optional[List[str]] = None,  # None for all roles
        task_name=None,
        help_text=''
):
    def real_decorator(func):
        nonlocal task_name

        if task_name is None:
            task_name = func.__name__

        func._roles = roles
        tasks.add_task(
            name=task_name,
            task=Task(func=func, name=task_name, roles=roles, help_text=help_text)
        )

        return func

    return real_decorator
