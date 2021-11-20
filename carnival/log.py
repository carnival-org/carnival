import typing

from carnival.host import Host


class _Writer(typing.Protocol):
    def write(self, __s: str) -> typing.Any: ...


def log(host: Host[typing.Any], message: str, file: typing.Optional[_Writer] = None) -> None:
    print(f"💃💃💃 {host.addr}> {message}", file=file)
