import typing
from carnival.task import TaskBase


class NoTask(TaskBase):
    def run(self, **kwargs: typing.Any) -> None:
        pass
