import typing
from invoke.context import Context  # type: ignore

from carnival.hosts import base


class LocalConnection(base.Connection):
    def __init__(self, host: base.Host) -> None:
        super().__init__(host)

        self._c: typing.Optional[Context] = None

    def __enter__(self) -> base.Connection:
        self._c = Context()
        return self

    def __exit__(self, *args: typing.Any) -> None:
        self._c = None

    def run(
        self,
        command: str,
        hide: bool = False, warn: bool = True, cwd: typing.Optional[str] = None,
    ) -> base.Result:
        assert self._c is not None, "Connection is not open"

        handler_kwargs = {
            "command": command,
            "hide": hide,
            "pty": True,
            "warn": warn,
        }

        handler = self._c.run

        if cwd is not None:
            with self._c.cd(cwd):
                return base.Result.from_invoke_result(handler(**handler_kwargs))

        return base.Result.from_invoke_result(handler(**handler_kwargs))


class LocalHost(base.Host):
    """
    Локальный хост, работает по локальному терминалу
    """

    addr: str = "local"
    """
    Адрес хоста, всегда `local`
    """

    def __init__(self, **context: typing.Any) -> None:
        """
        :param context: Контекст хоста
        """
        super().__init__(**context)
        self.addr = "local"

    def connect(self) -> LocalConnection:
        return LocalConnection(host=self)


localhost = LocalHost()
localhost_connection = localhost.connect().__enter__()
