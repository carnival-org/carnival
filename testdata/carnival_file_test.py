import typing
from carnival.task import Task


class NoTask(Task):
    def run(self, **kwargs: typing.Any) -> None:
        pass
