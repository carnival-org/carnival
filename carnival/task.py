import abc
import typing

from carnival.step import _underscore


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
