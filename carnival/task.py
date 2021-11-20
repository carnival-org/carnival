import abc
import re
import typing

from carnival.step import Step, ContextT
from carnival.host import Host


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


class Task(metaclass=abc.ABCMeta):
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

    def call_task(self, task_class: typing.Type['Task']) -> None:
        """
        Запустить другую задачу
        Возвращает результат работы задачи
        """
        task_class().run()

    @abc.abstractmethod
    def run(self) -> None:
        """
        Реализация выполнения задачи
        """
        raise NotImplementedError


class SimpleTask(typing.Generic[ContextT], Task, metaclass=abc.ABCMeta):
    hosts: typing.List[Host[ContextT]] = []
    steps: typing.List[typing.Type[Step[ContextT]]] = []

    def run(self) -> None:
        for host in self.hosts:
            for step in self.steps:
                print(f"💃💃💃 Running {self.get_name()}:{_underscore(step.__name__)} at {host}")
                step(host).run()
