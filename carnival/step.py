import abc
import typing

from carnival.host import AnyHost
from carnival.exceptions import StepValidationError


class Step:
    """
    Объект, предназначенный для выполнения группы комманд с какой-то целью.
    Вызывается из класса `carnival.Task` для выполнения комманд (`carnival.cmd`) на определенных хостах.

    Может требовать наличие определенных контекстных переменных для работы, указав их в аргументах метода `run`.
    Может вернуть значение для дальнейшего использования.

    В следующем примере переменная `disk_name` будет передана в run, а `install` пропущена.

    >>> host = Host(
    >>>     #  Адрес
    >>>     "1.2.3.4",
    >>>
    >>>     # Контекст хоста
    >>>     disk_name="/dev/sda1", install=['nginx', 'htop', ]
    >>> )
    >>> ...
    >>> class DiskUsage(Step):
    >>>     def run(self, disk_name: str):
    >>>         ...

    """
    def __init__(self) -> None:
        pass

    def validate(self, host: AnyHost) -> None:
        """
        Валидатор шага, запускается перед выполнением
        Должен выкидывать .StepValidationError в случае ошибки

        :param host: На котором будет выполнен шаг

        :raises StepValidationError: в случае ошибок валидации
        """
        raise StepValidationError("Step validation is not implemented")

    @abc.abstractmethod
    def run(self, host: AnyHost) -> typing.Any:
        """
        Метод который нужно определить для выполнения комманд

        :param host: Хост для выполнения шага
        """

        raise NotImplementedError
