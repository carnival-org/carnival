from typing import List, Dict, Any
from typing import no_type_check

import abc
import inspect

from carnival.host import Host

from carnival.secrets_manager import secrets_storage


def _get_arg_names(fn) -> List[str]:
    arg_names: List[str] = []
    spec = inspect.getfullargspec(fn)
    arg_names += spec.args
    arg_names += spec.kwonlyargs
    return arg_names


def _build_kwargs(fn, context: Dict[str, Any]):
    arg_names: List[str] = _get_arg_names(fn)
    kwargs = {}

    for context_name, context_val in context.items():
        if context_name in arg_names:
            kwargs[context_name] = context_val
    return kwargs


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
    def __init__(self, **context):
        """
        :param context: Переменные контекста, назначенные при вызове Шага
        """
        self.context = context

    def _build_context(self, host: Host) -> Dict[str, Any]:
        run_context = {'secrets': secrets_storage, 'host': host}
        if host.context:
            run_context.update(host.context)
        if self.context:
            run_context.update(self.context)
        return run_context

    def run_with_context(self, host: Host):
        context = self._build_context(host)
        kwargs = _build_kwargs(self.run, context)
        return self.run(**kwargs)

    @abc.abstractmethod
    @no_type_check
    def run(self, **kwargs):
        """
        Метод который нужно определить для выполнения комманд

        :param kwargs: Автоматические подставляемые переменные контекста
        """
        raise NotImplementedError
