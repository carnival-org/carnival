"""
Объект, представляющий единицу оборудования.

Carnival не предоставляет никаких сложных абстракций для работы с группами хостов,
подразумевая что вы будете использовать встроенные коллекции python и организуете
работу так, как будет удобно для вашей задачи.
В простом случае, можно передавать хосты прямо в коде файла `carnival_tasks.py`.
В более сложных, создать списки в отдельном файле, например `inventory.py`
"""

import typing
import abc
from dataclasses import dataclass

from invoke.context import Result as InvokeResult  # type: ignore


@dataclass
class Result:
    return_code: int
    ok: bool
    stdout: str
    stderr: str

    @classmethod
    def from_invoke_result(cls, invoke_result: InvokeResult) -> "Result":
        return Result(
            return_code=invoke_result.exited,
            ok=invoke_result.ok,
            stdout=invoke_result.stdout,
            stderr=invoke_result.stderr,
        )


class Connection:
    def __init__(self, host: "Host") -> None:
        self.host = host

    def __enter__(self) -> "Connection":
        raise NotImplementedError

    def __exit__(self, *args: typing.Any) -> None:
        pass

    @abc.abstractmethod
    def run(
        self,
        command: str,
        hide: bool = False, warn: bool = True, cwd: typing.Optional[str] = None,
    ) -> Result:
        """
        Запустить комманду

        См <https://docs.pyinvoke.org/en/latest/api/runners.html>
        """


class Host:
    """
    Локальный хост, работает по локальному терминалу

    :param context: Контекст хоста
    """

    def __init__(self, **context: typing.Any) -> None:
        self.addr = ""
        self.context = context
        self.context['host'] = self

    @abc.abstractmethod
    def connect(self) -> Connection:
        ...

    def __str__(self) -> str:
        return f"🖥 {self.addr}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.addr}>"
