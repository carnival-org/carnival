from dataclasses import dataclass
from typing import List, Union, Any, Type
import abc

import re

from carnival import global_context, Step

from carnival.host import Host


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


@dataclass
class TaskResult:
    host: Host
    step: Step
    result: Any


class Task:
    name: str = ""

    @classmethod
    def get_name(cls) -> str:
        return cls.name if cls.name else _underscore(cls.__name__)

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def call_task(self, task_class: Type['Task']):
        return task_class(dry_run=self.dry_run).run()

    def step(self, steps: Union[Step, List[Step]], hosts: Union[Host, List[Host]]) -> List[TaskResult]:
        if not isinstance(steps, list) and not isinstance(steps, tuple):
            steps = [steps, ]

        if not isinstance(hosts, list) and not isinstance(hosts, tuple):
            hosts = [hosts, ]

        results = []

        for host in hosts:
            global_context.set_context(host)

            for step in steps:
                step_name = _underscore(step.__class__.__name__)
                print(f"💃💃💃 Running {self.get_name()}:{step_name} at {host}")
                if not self.dry_run:
                    r = TaskResult(
                        host=host,
                        step=step,
                        result=step.run_with_context(host=host),
                    )
                    results.append(r)

            global_context.flush_context()
        return results

    def run(self):
        raise NotImplementedError


class SimpleTask(abc.ABC, Task):
    hosts: List[Host]
    steps: List[Step]

    def run(self):
        self.step(
            steps=self.steps,
            hosts=self.hosts,
        )
