import typing

from carnival import Connection
from carnival.steps import Step, validators


class SetHostname(Step):
    """
    Устанавливает hostname
    """

    def __init__(self, hostname: str) -> None:
        self.hostname = hostname

    def get_validators(self) -> typing.List["validators.StepValidatorBase"]:
        return [
            validators.CommandRequiredValidator('hostname'),
            validators.IsFileValidator('/etc/hostname'),
        ]

    def run(self, c: "Connection") -> typing.Any:
        c.run(f"echo '{self.hostname}' > /etc/hostname", use_sudo=True)
        c.run(f"hostname {self.hostname}", use_sudo=True)
