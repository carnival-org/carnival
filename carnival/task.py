import abc
import re
import typing

from carnival import Step
from carnival.host import AnyHost
from carnival.exceptions import StepValidationError


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


class TaskBase:
    """
    Задача это единица выполнения одного или несколькоих шагов на определенных хостах.

    Именование задач.

    Полное имя задачи состоит из двух частей. <module_name>.<name>.
    carnival автоматически генерирует имена задач из этих частей, но есть возможность управлять этим вручную,
    используя два атрибута класса Task.

    name:
    module_name:

    >>> class CheckDiskSpace(TaskBase):
    >>> help = "Print server root disk usage"
    >>>
    >>> def run(self, disk: str = "/") -> None:
    >>>    with connection.SetConnection(my_server):
    >>>        cmd.cli.run(f"df -h {disk}", hide=False)

    """

    # Имя задачи
    name: str = ""
    """
    название задачи. если не определено имя будет сгенерировано автоматически.
    """
    module_name: typing.Optional[str] = None
    """
    имя модуля. если назначить пустую строку, полное имя будет включать только название задачи.
    """

    help: str = ""
    """
    Строка помощи при вызове carnival help
    """

    @classmethod
    def get_name(cls) -> str:
        return cls.name if cls.name else _underscore(cls.__name__)

    def call_task(self, task_class: typing.Type['TaskBase']) -> typing.Any:
        """
        Запустить другую задачу
        Возвращает результат работы задачи
        """
        return task_class().run()

    def validate(self) -> typing.List[str]:
        """
        Хук для проверки валидности задачи перед запуском, не вызывается автоматически
        """

        return []

    @abc.abstractmethod
    def run(self) -> None:
        """
        Реализация выполнения задачи
        """
        raise NotImplementedError


class StepsTask(abc.ABC, TaskBase):
    """
    Запустить шаги `steps` на хостах `hosts`

    >>> class InstallPackages(StepsTask):
    >>>    help = "Install packages"
    >>>
    >>>    hosts = [my_server]
    >>>    steps = [InstallStep()]

    """

    hosts: typing.List[AnyHost]
    """
    Список хостов для выполнения шагов
    """

    @abc.abstractmethod
    def get_steps(self, host: AnyHost) -> typing.List[Step]:
        """
        Список шагов в порядке выполнения
        """
        raise NotImplementedError

    def validate(self) -> typing.List[str]:
        """
        Хук для проверки валидности задачи перед запуском, проверяет примеримость контекста хостов на шагах
        """

        from carnival.cli import carnival_tasks_module
        from carnival.tasks_loader import get_task_full_name

        errors: typing.List[str] = []

        for host in self.hosts:
            for step in self.get_steps(host):
                try:
                    step.validate(host=host)
                except StepValidationError as ex:
                    task_name = get_task_full_name(carnival_tasks_module, self.__class__)
                    step_name = step.__class__.__name__
                    errors.append(f"{task_name} -> {step_name} on {host}: {ex}")

        return errors

    def run(self) -> None:
        errors = self.validate()

        if errors:
            print("There is validation errors")
            for e in errors:
                print(f" * {e}")
            return

        for host in self.hosts:
            for step in self.get_steps(host):
                step_name = _underscore(step.__class__.__name__)
                print(f"💃💃💃 Running {self.get_name()}:{step_name} at {host}")
                step.run(host=host)
