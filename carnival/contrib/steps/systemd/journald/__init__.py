import typing

from carnival.steps import Step, validators
from carnival import Connection

from carnival.contrib.steps.transfer import PutTemplate


class DeployJournaldConfig(Step):
    """
    Заливает конфиг journald в /etc/systemd/journald.conf
    https://www.freedesktop.org/software/systemd/man/journald.conf.html
    """

    def __init__(
        self,
        config_template: str = 'carnival/contrib/steps/systemd/journald/journald.conf',
        directives: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> None:
        self.config_template = config_template
        self.context = {
            "directives": directives or {
                'SystemMaxFileSize': "10M",
            },
        }

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.TemplateValidator(self.config_template, self.context),
        ]

    def run(self, c: Connection) -> None:
        PutTemplate(
            self.config_template,
            '/etc/systemd/journald.conf',
            context=self.context,
        ).run(c)
        c.run("systemctl force-reload systemd-journald")
