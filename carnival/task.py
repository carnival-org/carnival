import abc
import re
import typing

from carnival.host._base import HostBaseT, ConnectionBaseT
from carnival.host import (
    SSHHost, SSHConnection,
    AnyHost, AnyConnection,
)


def _underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


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

    def __init__(self) -> None:
        pass

    def call_task(self, task_class: typing.Type['Task']) -> typing.Any:
        """
        Запустить другую задачу
        Возвращает результат работы задачи
        """
        return task_class().run()

    @abc.abstractmethod
    def run(self) -> typing.Any:
        """
        Реализация выполнения задачи
        """
        raise NotImplementedError


class TypedTask(typing.Generic[HostBaseT, ConnectionBaseT], Task, metaclass=abc.ABCMeta):
    """
    Запустить метод `host_run` хостах `self.hosts`

    Типизировання задача, позволяет задавать необходимый тип хоста и соединения с помощью generics

    .. versionadded:: 2.0

    >>> class LocalTask(TypedTask[YourHost, YourConnection]):
    >>>     hosts = [
    >>>         localhost, # mypy error
    >>>         SSHHost("1.2.3.4"),  # mypy error
    >>>         YourHost(),        # OK
    >>>     ]
    >>>     def host_run(self):
    >>>         cmd.cli.run(self.c, self.host.command)
    """

    hosts: typing.List[HostBaseT]  #: Список хостов для выполнения
    c: ConnectionBaseT  #: соединение с хостом
    host: HostBaseT  #: хост с которым в данный момент соединен

    def run(self) -> None:
        for host in self.hosts:
            with host.connect() as c:
                self.host = host
                self.c = c  # type: ignore  # https://github.com/python/mypy/issues/3151
                self.host_run()

    @abc.abstractmethod
    def host_run(self) -> None:
        """
        Реализация выполнения задачи
        HostConnection доступен через `self.c`
        """
        raise NotImplementedError


class SSHTask(TypedTask[SSHHost, SSHConnection], metaclass=abc.ABCMeta):
    """
    Запустить метод `host_run` хостах `self.hosts`, типизировано для ssh хостов
    .. versionadded:: 2.0
    """


class AnyTask(TypedTask[AnyHost, AnyConnection], metaclass=abc.ABCMeta):
    """
    Запустить метод `host_run` хостах `self.hosts`, типизировано для любых хостов
    .. versionadded:: 2.0
    """


__all__ = [
    "Task",
    "TypedTask",
    "SSHTask",
    "AnyTask",
]
