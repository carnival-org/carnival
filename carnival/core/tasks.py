from typing import List, Dict, Optional


class Task:
    def __init__(self, func, name: str, roles: List[str], help_text=''):
        self.func = func
        self.roles = roles
        self.help_text = help_text
        self.name = name

    def __str__(self):
        return f"⛏{self.name}"

    def run(self):
        self.func()


class Tasks:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def add_task(self, name: str, task: Task):
        if name in self._tasks:
            raise ValueError(f"Task {name} already exist.")

        self._tasks[name] = task

    def items(self):
        return self._tasks.items()

    def get_task(self, name) -> Optional[Task]:
        return self._tasks.get(name, None)
