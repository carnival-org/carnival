import typing
import os
from carnival.host import AnyHost


class _Writer(typing.Protocol):
    def write(self, __s: str) -> typing.Any: ...


def log(message: str, host: typing.Optional[AnyHost], file: typing.Optional[_Writer] = None) -> None:
    if host is None:
        host_part = "NO CONNECTION"
    else:
        host_part = str(host)

    print(f"💃💃💃 {host_part}> {message}", file=file)


def envvar(varname: str) -> str:
    if varname not in os.environ:
        raise ValueError(f"{varname} is not persent in environment")

    return os.environ[varname]
