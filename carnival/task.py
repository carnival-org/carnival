import abc
import re
import typing
import sys

from carnival import Step
from carnival.role import Role
from carnival.exceptions import StepValidationError
from carnival.utils import log


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
    >>>     help = "Print server root disk usage"
    >>>
    >>>     def run(self) -> None:
    >>>         with my_server.connect() as c:
    >>>             cmd.cli.run(f"df -h /", hide=False)

    """

    # Имя задачи
    name: typing.ClassVar[str] = ""
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

    def __init__(self, no_validate: bool) -> None:
        self.no_validate = no_validate

    @classmethod
    def get_name(cls) -> str:
        return cls.name if cls.name else _underscore(cls.__name__)

    def call_task(self, task_class: typing.Type['TaskBase']) -> typing.Any:
        """
        Запустить другую задачу
        Возвращает результат работы задачи
        """
        return task_class(no_validate=self.no_validate).run()

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


RoleT = typing.TypeVar("RoleT", bound=Role)


class Task(typing.Generic[RoleT], abc.ABC, TaskBase):
    """
    Запустить шаги `steps` на хостах `hosts`

    >>> class InstallPackages(Task):
    >>>    help = "Install packages"
    >>>
    >>>    hosts = [my_server]
    >>>    steps = [InstallStep(my_server.context['packages'])]

    """

    role: RoleT
    """
    Роль, доступная в методе `.get_steps`
    """

    def __init__(self, no_validate: bool) -> None:
        super().__init__(no_validate=no_validate)
        # Get role from generic
        self.role_class: typing.Type[RoleT] = typing.get_args(self.__class__.__orig_bases__[0])[0]  # type: ignore
        self.hostroles: typing.List[RoleT] = self.role_class.resolve()
        if not self.hostroles:
            print(f"[WARN]: not hosts for {self.role_class}", file=sys.stderr)

    @abc.abstractmethod
    def get_steps(self) -> typing.List[Step]:
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

        for hostrole in self.hostroles:
            with hostrole.host.connect() as c:
                self.role = hostrole
                for step in self.get_steps():
                    try:
                        step.validate(c=c)
                    except StepValidationError as ex:
                        task_name = get_task_full_name(carnival_tasks_module, self.__class__)
                        step_name = step.get_name()
                        errors.append(f"{task_name} -> {step_name} on {hostrole.host}: {ex}")
                del self.role

        return errors

    def run(self) -> None:
        from carnival.cli import carnival_tasks_module
        from carnival.tasks_loader import get_task_full_name

        if not self.no_validate:
            errors = self.validate()

            if errors:
                print("There is validation errors")
                for e in errors:
                    print(f" * {e}")
                return

        for hostrole in self.hostroles:
            with hostrole.host.connect() as c:
                self.role = hostrole
                for step in self.get_steps():
                    task_name = get_task_full_name(carnival_tasks_module, self.__class__)
                    step_name = step.get_name()
                    log(f"Running {task_name}:{step_name}", host=hostrole.host)
                    step.run(c=c)
