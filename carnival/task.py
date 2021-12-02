import abc
import re
import typing
import sys

from colorama import Fore, Style, Back  # type: ignore

from carnival import Step
from carnival.role import Role
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

    def call_task(self, task_class: typing.Type['TaskBase']) -> bool:
        """
        Запустить другую задачу
        Возвращает результат работы задачи
        """
        task = task_class(no_validate=self.no_validate)
        is_valid = task.validate()
        if is_valid:
            task.run()

        return is_valid

    def validate(self) -> bool:
        """
        Хук для проверки валидности задачи перед запуском, не вызывается автоматически
        """

        return True

    @abc.abstractmethod
    def run(self) -> None:
        """
        Реализация выполнения задачи
        """
        raise NotImplementedError


RoleT = typing.TypeVar("RoleT", bound=Role)


class Task(abc.ABC, typing.Generic[RoleT], TaskBase):
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

    def validate(self) -> bool:
        """
        Хук для проверки валидности задачи перед запуском, проверяет примеримость контекста хостов на шагах
        """
        if self.no_validate:
            return True

        from carnival.cli import carnival_tasks_module
        from carnival.tasks_loader import get_task_full_name
        task_name = get_task_full_name(carnival_tasks_module, self.__class__)
        print(f"Validating task {Style.BRIGHT}{Fore.BLUE}{task_name}{Fore.RESET}{Style.RESET_ALL}", end="", flush=True)
        errors: typing.List[str] = []

        for hostrole in self.hostroles:
            with hostrole.host.connect() as c:
                self.role = hostrole
                for step in self.get_steps():
                    try:
                        step.validate(c=c)
                        print(f"{Fore.GREEN}.{Fore.RESET}", end="", flush=True)
                    except StepValidationError as ex:
                        step_name = step.get_name()
                        errors.append(f"{task_name} -> {step_name} on {hostrole.host}: {Fore.RED}{ex}{Fore.RESET}")
                        print("{Fore.RED}e{Fore.RESET}", end="", flush=True)
                del self.role

        if errors:
            print(f" {Fore.RED}{len(errors)} errors{Fore.RESET}")
            for e in errors:
                print(f" * {e}")
            return False

        print(f" {Style.BRIGHT}{Fore.GREEN}OK{Fore.RESET}{Style.RESET_ALL}")
        return True

    def run(self) -> None:
        from carnival.cli import carnival_tasks_module
        from carnival.tasks_loader import get_task_full_name

        for hostrole in self.hostroles:
            with hostrole.host.connect() as c:
                self.role = hostrole
                for step in self.get_steps():
                    task_name = get_task_full_name(carnival_tasks_module, self.__class__)
                    step_name = step.get_name()
                    print(f"{Back.YELLOW}💃💃💃{Back.BLUE} {hostrole.host}{Back.RESET}{Fore.RESET}> Running {Style.BRIGHT}{task_name}:{step_name}{Style.RESET_ALL}")
                    step.run(c=c)
