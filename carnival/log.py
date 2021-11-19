import typing

from carnival.host import AnyHost


class _Writer(typing.Protocol):
    def write(self, __s: str) -> typing.Any: ...


def log(host: AnyHost[typing.Any], message: str, file: typing.Optional[_Writer] = None) -> None:
    print(f"💃💃💃 {host.addr}> {message}", file=file)
