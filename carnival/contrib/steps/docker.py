import os
import typing

from colorama import Fore as F, Style as S  # type: ignore

from carnival import Step
from carnival import Connection
from carnival.steps import validators, shortcuts

from carnival.contrib.steps import apt, systemd


class CeInstallUbuntu(Step):
    """
    Установить docker на ubuntu
    https://docs.docker.com/engine/install/ubuntu/
    """
    def __init__(self, docker_version: typing.Optional[str] = None) -> None:
        """
        :param docker_version: версия docker-ce
        """
        self.docker_version = docker_version

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator("apt-get"),
            validators.CommandRequiredValidator("curl"),
        ]

    def run(self, c: Connection) -> None:
        pkgname = "docker-ce"
        if apt.IsPackageInstalled(pkgname=pkgname, version=self.docker_version).run(c=c):
            print(f"{S.BRIGHT}docker-ce{S.RESET_ALL}: {F.GREEN}already installed{F.RESET}")

        print(f"Installing {pkgname}...")
        c.run("sudo apt-get update")
        c.run("sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common")
        c.run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
        c.run('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')  # noqa:E501

        apt.ForceInstall(pkgname=pkgname, version=self.docker_version, update=True, hide=True).run(c=c)
        print(f"{S.BRIGHT}docker-ce{S.RESET_ALL}: {F.YELLOW}installed{F.RESET}")


class ComposeInstall(Step):
    """
    Установить docker-compose
    """
    def __init__(
        self,
        version: str = "1.25.1",
        dest: str = "/usr/bin/docker-compose",
    ) -> None:
        """
        :param version: версия compose
        :param dest: папка для установки, позразумевается что она должна быт в $PATH
        """
        self.version = version
        self.dest = dest

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator("curl"),
        ]

    def run(self, c: Connection) -> None:
        if shortcuts.is_cmd_exist(c, "docker-compose"):
            print(f"{S.BRIGHT}docker-compose{S.RESET_ALL}: {F.GREEN}already installed{F.RESET}")
            return

        link = f"https://github.com/docker/compose/releases/download/{self.version}/docker-compose-`uname -s`-`uname -m`"  # noqa:501
        c.run(f"sudo curl -sL {link} -o {self.dest}")
        c.run(f"sudo chmod a+x {self.dest}")
        print(f"{S.BRIGHT}docker-compose{S.RESET_ALL}: {F.GREEN}already installed{F.RESET}")


class UploadImageFile(Step):
    """
    Залить с локаьного диска tar-образ docker на сервер
    и загрузить в демон командой `docker save image -o image.tar`
    """
    def __init__(
        self,
        docker_image_path: str,
        dest_dir: str = '/tmp/',
        rm_after_load: bool = False,
        rsync_opts: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        """
        :param docker_image_path: tar-образ docker
        :param dest_dir: папка куда заливать
        :param rm_after_load: удалить образ после загрузки
        """
        if not dest_dir.endswith("/"):
            dest_dir += "/"

        self.docker_image_path = docker_image_path
        self.dest_dir = dest_dir
        self.rm_after_load = rm_after_load
        self.rsync_opts = rsync_opts or {}

    def get_name(self) -> str:
        return f"{super().get_name()}(src={self.docker_image_path}, dst={self.dest_dir})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator("systemctl"),
            validators.CommandRequiredValidator("docker"),
        ]

    def run(self, c: Connection) -> None:
        image_file_name = os.path.basename(self.docker_image_path)
        systemd.Start("docker").run(c=c)

        shortcuts.rsync(c.host, self.docker_image_path, self.dest_dir, **self.rsync_opts)
        c.run(f"cd {self.dest_dir}; docker load -i {image_file_name}")

        if self.rm_after_load:
            c.run(f"rm -rf {self.dest_dir}{image_file_name}")
