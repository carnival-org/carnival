import abc
import re
from dataclasses import dataclass
import copy
import typing

from carnival import Step, global_context
from carnival.host import AnyHost


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


@dataclass
class TaskResult:
    """
    Возвращается вызовом метода Task.step
    """
    host: AnyHost
    """
    Хост на котором выполнялся шаг
    """
    step: Step
    """
    Шаг
    """
    result: typing.Any
    """
    Результат выполения шага
    """


class Task:
    """
    Задача это единица выполнения одного или несколькоих шагов на определенных хостах.

    Именование задач.

    Полное имя задачи состоит из двух частей. <module_name>.<name>.
    carnival автоматически генерирует имена задач из этих частей, но есть возможность управлять этим вручную,
    используя два атрибута класса Task.

    name: название задачи. если не определено имя будет сгенерировано автоматически.
    module_name: имя модуля. если назначить пустую строку, полное имя будет включать только название задачи.
    """

    # Имя задачи
    name: str = ""
    module_name: typing.Optional[str] = None
    help: str = ""

    @classmethod
    def get_name(cls) -> str:
        return cls.name if cls.name else _underscore(cls.__name__)

    def call_task(self, task_class: typing.Type['Task']) -> typing.Any:
        """
        Запустить другую задачу
        Возвращает результат работы задачи
        """
        return task_class().run()

    def extend_host_context(self, host: AnyHost) -> typing.Dict[str, typing.Any]:
        """
        Метод для переопределения контекста хоста, вызываемый методом `.step` по умолчанию контекст не переопределяется

        :param host: хост на котором готовится запуск
        """
        return copy.deepcopy(host.context)

    def step(self, steps: typing.List[Step], hosts: typing.List[AnyHost]) -> typing.List[TaskResult]:
        """
        Запустить шаг(и) на хост(ах)
        Возвращает объект TaskResult для получения результатов работы каждого шага на каждом хосте
        """

        results = []

        for host in hosts:
            with global_context.SetContext(host):
                for step in steps:
                    step_name = _underscore(step.__class__.__name__)
                    print(f"💃💃💃 Running {self.get_name()}:{step_name} at {host}")
                    r = TaskResult(
                        host=host,
                        step=step,
                        result=step.run_with_context(self.extend_host_context(host=host)),
                    )
                    results.append(r)
        return results

    @abc.abstractmethod
    def run(self) -> typing.Any:
        """
        Реализация выполнения задачи
        """
        raise NotImplementedError


class SimpleTask(abc.ABC, Task):
    """
    Запустить шаги `steps` на хостах `hosts`
    """

    hosts: typing.List[AnyHost]
    """
    Список хостов
    """
    steps: typing.List[Step]
    """
    Список шагов в порядке выполнения
    """

    def run(self) -> None:
        self.step(
            steps=self.steps,
            hosts=self.hosts,
        )
