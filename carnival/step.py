import abc
import typing


if typing.TYPE_CHECKING:
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
    def __init__(self) -> None:
        pass

    def validate(self, c: "Connection") -> None:
        """
        Валидатор шага, запускается перед выполнением
        Должен выкидывать .StepValidationError в случае ошибки

        :param host: На котором будет выполнен шаг

        :raises StepValidationError: в случае ошибок валидации

        >>> from carnival.exceptions import StepValidationError
        >>> ...
        >>> def validate(self, c: "Connection") -> None:
        >>>     raise StepValidationError("Step validation is not implemented")
        """
        pass

    @abc.abstractmethod
    def run(self, c: "Connection") -> typing.Any:
        """
        Метод который нужно определить для выполнения команд

        :param c: Соединение с хостом для выполнения шага
        """

        raise NotImplementedError
