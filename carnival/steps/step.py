import abc
import typing

if typing.TYPE_CHECKING:
    from carnival.steps.validators import StepValidatorBase
    from carnival import Connection


class Step:
    """
    Объект, предназначенный для выполнения группы команд с какой-то целью.
    Вызывается из класса `carnival.Task` для выполнения команд (`carnival.cmd`) на определенных хостах.

    Может требовать наличие определенных контекстных переменных для работы, указав их в аргументах конструктора,
    а в задаче (Task) передать нужные аргументы в конструктор.

    Может вернуть значение для дальнейшего использования.

    >>> ...
    >>> class DiskUsage(Step):
    >>>     def __init__(self, disk_name: str):
    >>>         self.disk_name = disk_name
    >>>
    >>>     def run(self, c: Connection):
    >>>         ...

    """

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_validators(self) -> typing.List["StepValidatorBase"]:
        """
        Получить список валидаторов для метода `.validate`
        """
        return []

    def validate(self, c: "Connection") -> typing.List[str]:
        """
        Валидатор шага, запускается перед выполнением
        :param c: Конект к хосту
        :return: Список ошибок
        """

        errors: typing.List[str] = []

        for validator in self.get_validators():
            err = validator.validate(c=c)
            if err is not None:
                errors.append(err)

        return errors

    @abc.abstractmethod
    def run(self, c: "Connection") -> typing.Any:
        """
        Метод который нужно определить для выполнения команд

        :param c: Соединение с хостом для выполнения шага
        """

        raise NotImplementedError


T = typing.TypeVar("T")


class InlineStep(typing.Generic[T], Step):
    """
    Шаг, который можно создать прямо внутри задачи

    >>> from carnival import Task
    >>>
    >>> class InstallPackages(Task):
    >>>    help = "Install packages"
    >>>
    >>>    hosts = [my_server]
    >>>    def get_steps(self) -> typing.List["Step"]:
    >>>        return [
    >>>            InlineStep("install_packages", lambda c: c.run("apt-get install htop"))
    >>>        ]

    """
    def __init__(self, name: str, fn: typing.Callable[["Connection", ], T]) -> None:
        """
        :param name: имя шага которое выводится в консоли при запуске шага
        :param fn: функция которая будет вызвана при запуске шага, возвращаемое значение вернется из шага
        """
        self.fn = fn
        self.name = name

    def get_name(self) -> str:
        return self.name

    def run(self, c: "Connection") -> T:
        return self.fn(c)
