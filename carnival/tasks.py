from typing import List

from carnival.context import tasks
from carnival.core.tasks import Task

ROLE_ALL = ['all', ]


def task(roles: List[str], task_name=None, help_text=''):
    def real_decorator(func):
        nonlocal task_name

        if task_name is None:
            task_name = func.__name__

        func._roles = roles
        tasks.add_task(
            name=task_name,
            task=Task(func=func, roles=roles, help_text=help_text)
        )

        return func

    return real_decorator


@task(roles=ROLE_ALL)
def tasks_list():
    for name, t in tasks.items():
        print(f" * {name} [{','.join(t.roles)}]", end="")

        if t.help_text:
            print(" - {t.help_text}")
        else:
            print()
