"""
Задача это единица выполнения одного или несколькоих шагов на определенных хостах.

Именование задач.
=================

Полное имя задачи состоит из двух частей. <module_name>.<name>.
carnival автоматически генерирует имена задач из этих частей, но есть возможность управлять этим вручную,
используя два атрибута класса Task.
"""

import abc
import re
import typing
import sys

from colorama import Fore as F, Style as S, Back as B  # type: ignore

if typing.TYPE_CHECKING:
    from carnival.role import Role
    from carnival import Step


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


class TaskBase:
    """
    Базовый обьект задачи

    >>> from carnival import SshHost
    >>>
    >>> my_server = SshHost("192.168.1.10")
    >>>
    >>> class CheckDiskSpace(TaskBase):
    >>>     help = "Print server root disk usage"
    >>>
    >>>     def run(self) -> None:
    >>>         with my_server.connect() as c:
    >>>             c.run(f"df -h /", hide=False)

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


RoleT = typing.TypeVar("RoleT", bound="Role")


class Task(abc.ABC, typing.Generic[RoleT], TaskBase):
    """
    Задача роли

    >>> from carnival import SshHost, Role
    >>> from my_steps import InstallStep
    >>>
    >>> my_server = SshHost("192.168.1.10")
    >>>
    >>> class MyRole(Role):  # Определяем роль
    >>>     packages = ['htop', 'mc']
    >>>
    >>>
    >>> class Install(Task[MyRole]):  # определяем задачу для этой роли
    >>>    help = "Install packages"
    >>>
    >>>    hosts = [my_server]
    >>>
    >>>    def get_steps(self) -> typing.List["Step"]:
    >>>        return [
    >>>            InstallStep(self.role.packages)
    >>>        ]
    >>>
    """

    role: RoleT
    """
    Роль, доступная в методе :py:meth:`~Task.get_steps`

    Задачи привязываются к ролям через указание generic-типа

    >>> from carnival import Task
    >>>
    >>> class DeployNginx(Task[NginxRole]):
    >>>     ...
    """

    def __init__(self, no_validate: bool) -> None:
        super().__init__(no_validate=no_validate)
        # Get role from generic
        self.role_class: typing.Type[RoleT] = typing.get_args(self.__class__.__orig_bases__[0])[0]  # type: ignore
        self.hostroles: typing.List[RoleT] = self.role_class.resolve()
        if not self.hostroles:
            print(f"[WARN]: not hosts for {self.role_class}", file=sys.stderr)

    @abc.abstractmethod
    def get_steps(self) -> typing.List["Step"]:
        """
        Список шагов в порядке выполнения
        """
        raise NotImplementedError

    def validate(self) -> bool:
        if self.no_validate:
            return True

        from carnival.cli import carnival_tasks_module
        from carnival.tasks_loader import get_task_full_name
        task_name = get_task_full_name(carnival_tasks_module, self.__class__)
        print(f"Validating task {S.BRIGHT}{F.BLUE}{task_name}{F.RESET}{S.RESET_ALL} ", end="", flush=True)
        errors: typing.List[str] = []

        for hostrole in self.hostroles:
            with hostrole.host.connect() as c:
                self.role = hostrole
                for step in self.get_steps():
                    step_errors = step.validate(c=c)

                    if not step_errors:
                        print(f"{F.GREEN}.{F.RESET}", end="", flush=True)
                    else:
                        step_name = step.get_name()
                        for e in step_errors:
                            errors.append(f"{task_name} -> {step_name} on {hostrole.host}: {F.RED}{e}{F.RESET}")
                        print(f"{F.RED}e{F.RESET}", end="", flush=True)
                del self.role

        if errors:
            print(f" {F.RED}{len(errors)} errors{F.RESET}")
            for e in errors:
                print(f" * {e}")
            return False

        print(f" {S.BRIGHT}{F.GREEN}OK{F.RESET}{S.RESET_ALL}")
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
                    print(
                        f"{B.YELLOW}💃💃💃{B.BLUE} {hostrole.host}{B.RESET}{F.RESET}> "
                        f"Running {S.BRIGHT}{task_name}:{step_name}{S.RESET_ALL}"
                    )
                    step.run(c=c)
