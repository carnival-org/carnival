import os
import typing
from itertools import chain

from carnival import Connection
from carnival import Step
from carnival.steps import validators

from carnival.contrib.steps import systemd, transfer


class UploadService(Step):
    """
    Залить docker-compose сервис и запустить
    """

    def __init__(
            self,
            app_dir: str,

            template_files: typing.List[typing.Union[str, typing.Tuple[str, str]]],
            template_context: typing.Dict[str, typing.Any],
    ):
        """
        :param app_dir: Путь до папки назначения
        :param template_files: Список jinja2-шаблонов. Может быть списком файлов или кортежей (src, dst)
        :param template_context: Контекст шаблонов, один на все шаблоны
        """
        self.app_dir = app_dir

        self.template_files: typing.List[typing.Tuple[str, str]] = []
        for dest in template_files:
            if isinstance(dest, str):
                template_path = dest
                dest_fname = os.path.basename(template_path)
            elif isinstance(dest, tuple):
                template_path, dest_fname = dest
            else:
                raise ValueError(f"Cant parse template_file definition: {dest}")

            self.template_files.append((template_path, dest_fname))

        self.template_context = template_context

        self.transfer_chain = []
        for template_path, dest_fname in self.template_files:
            self.transfer_chain.append(transfer.PutTemplate(
                template_path=template_path,
                remote_path=os.path.join(self.app_dir, dest_fname),
                context=self.template_context,
            ))

    def get_name(self) -> str:
        return f"{super().get_name()}({self.app_dir})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            *list(chain(*[x.get_validators() for x in self.transfer_chain])),
            validators.CommandRequiredValidator('docker'),
            validators.CommandRequiredValidator('docker-compose'),
        ]

    def run(self, c: Connection) -> typing.Any:
        systemd.Start("docker").run(c=c)

        c.run(f"mkdir -p {self.app_dir}")

        for transfer_step in self.transfer_chain:
            transfer_step.run(c)

        c.run("docker-compose rm -f", cwd=self.app_dir, hide=True)


class Up(Step):
    def __init__(
        self,
        app_dir: str,
        scale: typing.Optional[typing.Dict[str, int]] = None,
        only: typing.Optional[typing.List[str]] = None
    ):
        """
        :param app_dir: Путь до папки назначения
        :param scale: Масштабирование сервисов при запуске, не используется если `None`
        :param only: Запустить только указанные сервисы, не используется если `None`
        """
        self.app_dir = app_dir
        self.scale = scale
        self.only = only

    def get_name(self) -> str:
        return f"{super().get_name()}({self.app_dir})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.InlineValidator(
                if_err_true_fn=lambda c: self.only == [],
                error_message="'only' must not be empty list, use None to disable",
            ),
            validators.CommandRequiredValidator('docker'),
            validators.CommandRequiredValidator('docker-compose'),
        ]

    def run(self, c: Connection) -> typing.Any:
        systemd.Start("docker").run(c=c)

        onlystr = ""
        if self.only is not None:
            onlystr = " ".join(self.only)

        if self.scale:
            scale_str = " ".join([f" --scale {service_name}={count}" for service_name, count in self.scale.items()])
        else:
            scale_str = ""
        c.run(f"docker-compose up -d --remove-orphans {onlystr} {scale_str}", cwd=self.app_dir)


class Ps(Step):
    """
    docker-compose ps
    """

    subcommand = "ps"

    def __init__(self, app_dir: str, flags: str = ""):
        """
        :param app_dir: Application remote directory
        """
        self.app_dir = app_dir
        self.flags = flags

    def get_name(self) -> str:
        return f"{super().get_name()}({self.app_dir})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('docker-compose'),
        ]

    def run(self, c: Connection) -> typing.Any:
        c.run(f"docker-compose {self.subcommand} {self.flags}", cwd=self.app_dir)


class Restart(Ps):
    """
    docker-compose restart
    """

    subcommand = "restart"


class RestartServices(Step):
    """
    docker-compose restart [services...]
    """

    subcommand = "restart"

    def __init__(self, app_dir: str, services: typing.List[str]):
        """
        :param app_dir: Application remote directory
        """
        self.app_dir = app_dir
        self.services = " ".join(services)
        self.services = self.services.strip()

    def get_name(self) -> str:
        return f"{super().get_name()}(services='{self.services}')"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.InlineValidator(
                if_err_true_fn=lambda c: not self.services,
                error_message="'services' must not be empty",
            ),
            validators.CommandRequiredValidator('docker-compose'),
        ]

    def run(self, c: Connection) -> typing.Any:
        c.run(f"docker-compose {self.subcommand} {self.services}", cwd=self.app_dir)


class Stop(Ps):
    """
    docker-compose stop
    """
    subcommand = "stop"


class StopServices(RestartServices):
    """
    docker-compose logs -f --tail=tail
    """
    subcommand = "stop"


class Logs(Step):
    """
    docker-compose restart [services...]
    """

    def __init__(self, app_dir: str, tail: int = 20):
        """
        :param app_dir: Application remote directory
        """
        self.app_dir = app_dir
        self.tail = tail

    def get_name(self) -> str:
        return f"{super().get_name()}({self.app_dir})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('docker-compose'),
        ]

    def run(self, c: Connection) -> typing.Any:
        c.run(f"docker-compose logs -f --tail={self.tail}", cwd=self.app_dir, hide=False)


class LogsServices(Step):
    """
    docker-compose logs -f --tail=tail [services...]
    """

    def __init__(self, app_dir: str, services: typing.List[str], tail: int = 20):
        """
        :param app_dir: Application remote directory
        """
        self.app_dir = app_dir
        self.services = " ".join(services)
        self.services = self.services.strip()
        self.tail = tail

    def get_name(self) -> str:
        return f"{super().get_name()}(services='{self.services}')"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.InlineValidator(
                if_err_true_fn=lambda c: not self.services,
                error_message="'services' must not be empty",
            ),
            validators.CommandRequiredValidator('docker-compose'),
        ]

    def run(self, c: Connection) -> typing.Any:
        c.run(f"docker-compose logs -f --tail={self.tail} {self.services}", cwd=self.app_dir)
