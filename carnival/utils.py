import typing
import os
from carnival import Host


class _Writer(typing.Protocol):
    def write(self, __s: str) -> typing.Any: ...


def log(message: str, host: typing.Optional[Host], file: typing.Optional[_Writer] = None) -> None:
    if host is None:
        host_part = "NO CONNECTION"
    else:
        host_part = str(host)

    print(f"💃💃💃 {host_part}> {message}", file=file)


def envvar(varname: str) -> str:
    """
    Получить переменную из окружения
    Замена context_ref для carnival v3
    :raises: ValueError если переменной в окружении нет
    """

    if varname not in os.environ:
        raise ValueError(f"{varname} is not persent in environment")

    return os.environ[varname]
