import typing

from carnival import Connection
from carnival.steps import Step, validators, shortcuts


class SetHostname(Step):
    """
    Устанавливает hostname
    """

    def __init__(self, hostname: str) -> None:
        self.hostname = hostname

    def get_name(self) -> str:
        return f"{super().get_name()}(hostname={self.hostname})"

    def get_validators(self) -> typing.List["validators.StepValidatorBase"]:
        return [
            validators.CommandRequiredValidator('hostname'),
            validators.IsFileValidator('/etc/hostname'),
        ]

    def run(self, c: "Connection") -> typing.Any:
        c.run(f"echo '{self.hostname}' > /etc/hostname", use_sudo=True)
        c.run(f"hostname {self.hostname}", use_sudo=True)


class SetTimezone(Step):
    """
    Устанавливает таймзону через timedatectl

    https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    """
    def __init__(self, timezone: str = 'Etc/UTC') -> None:
        self.timezone = timezone

    def get_validators(self) -> typing.List["validators.StepValidatorBase"]:
        return [
            validators.CommandRequiredValidator('dpkg-reconfigure'),
        ]

    def run(self, c: "Connection") -> typing.Any:
        if not shortcuts.is_file_contains(c, '/etc/timezone', self.timezone):
            c.run(f'timedatectl set-timezone {self.timezone}')
            self.log_action("timezone set", self.timezone)
