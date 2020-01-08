from typing import List, Dict


class Task:
    def __init__(self, func, roles: List[str], help_text=''):
        self.func = func
        self.roles = roles
        self.help_text = help_text

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

    def run_task(self, name):
        return self._tasks[name].run()
