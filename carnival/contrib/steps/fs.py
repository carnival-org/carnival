import typing

from carnival import Step, Connection
from carnival.steps import validators


class Mkdirs(Step):
    """
    Создать папки
    """

    def __init__(self, paths: typing.List[str]):
        """
        :param paths: папки
        """
        self.paths = paths

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator("mkdir")
        ]

    def run(self, c: Connection) -> None:
        for path in self.paths:
            c.run(f"mkdir -p {path}")


class Sync(Step):
    """
    Запускает sync
    """

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator("sync")
        ]

    def run(self, c: "Connection") -> typing.Any:
        c.run("sync")
