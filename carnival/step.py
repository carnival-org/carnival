import abc
from typing import Any, no_type_check

from carnival.context import build_context, build_kwargs
from carnival.host import AnyHost


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
    def __init__(self, **context: Any):
        """
        :param context: Переменные контекста, назначенные при вызове Шага
        """
        self.context = context

    def run_with_context(self, host: AnyHost) -> Any:
        context = build_context(self, host)
        kwargs = build_kwargs(self.run, context)
        return self.run(**kwargs)  # type: ignore

    @abc.abstractmethod
    @no_type_check
    def run(self, **kwargs) -> None:
        """
        Метод который нужно определить для выполнения комманд

        :param kwargs: Автоматические подставляемые переменные контекста, поддерживается `**kwargs`
        """

        raise NotImplementedError
