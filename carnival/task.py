import abc
import re
import copy
import typing

from carnival import Step, connection
from carnival.host import AnyHost
from carnival.exceptions import ContextBuilderError


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
    Список хостов
    """
    steps: typing.List[Step]
    """
    Список шагов в порядке выполнения
    """

    def extend_host_context(self, host: AnyHost) -> typing.Dict[str, typing.Any]:
        """
        Метод для переопределения контекста хоста

        :param host: хост на котором готовится запуск
        """
        return copy.deepcopy(host.context)

    def validate(self) -> typing.List[str]:
        """
        Хук для проверки валидности задачи перед запуском, проверяет примеримость контекста хостов на шагах
        """

        errors: typing.List[str] = []

        for host in self.hosts:
            for step in self.steps:
                try:
                    step.run_with_context(self.extend_host_context(host=host))
                except ContextBuilderError as ex:
                    errors.append(f"{self.__class__.__qualname__} -> {step.__class__.__qualname__} on {host}: {ex}")

        return errors

    def run(self) -> None:
        errors = self.validate()

        if errors:
            print("There is context building errors")
            for e in errors:
                print(f" * {e}")
            return

        for host in self.hosts:
            host_ctx = self.extend_host_context(host=host)
            with connection.SetConnection(host):
                for step in self.steps:
                    step_name = _underscore(step.__class__.__name__)
                    print(f"💃💃💃 Running {self.get_name()}:{step_name} at {host}")
                    call_step = step.run_with_context(host_ctx)
                    call_step()
