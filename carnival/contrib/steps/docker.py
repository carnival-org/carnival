import os
import typing

from carnival import Step
from carnival import Connection
from carnival.steps import validators, shortcuts

from carnival.contrib.steps import apt, systemd, transfer


class CeInstallUbuntu(Step):
    """
    Установить docker на ubuntu
    https://docs.docker.com/engine/install/ubuntu/

    Автоматически подставляет архитектуру, используя `dpkg --print-architecture`
    """
    def __init__(self, version: typing.Optional[str] = None) -> None:
        """
        :param version: версия docker-ce
        """
        self.version = version

    def get_name(self) -> str:
        return f"{super().get_name()}(version={self.version or 'any'})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator("dpkg"),
            validators.CommandRequiredValidator("lsb_release"),
            validators.CommandRequiredValidator("apt-get"),
        ]

    def run(self, c: Connection) -> None:
        pkgname = "docker-ce"
        if apt.IsPackageInstalled(pkgname=pkgname, version=self.version).run(c=c):
            return

        apt.InstallMultiple(
            ["apt-transport-https", "ca-certificates", "curl", "software-properties-common"],
            update=True
        ).run(c)

        c.run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -", hide=True)

        arch_type = c.run("dpkg --print-architecture").stdout.strip()

        c.run(
            f'add-apt-repository -y "deb [arch={arch_type}] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',  # noqa:E501
            hide=True
        )
        apt.Update().run(c)
        apt.Install(pkgname, version=self.version, update=False).run(c)


class ComposeInstall(Step):
    """
    Установить docker-compose
    """
    def __init__(
        self,
        version: str = "v2.2.2",
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
            validators.CommandRequiredValidator("uname"),
        ]

    def run(self, c: Connection) -> None:
        if shortcuts.is_cmd_exist(c, "docker-compose"):
            return

        kernel = c.run("uname -s").stdout.strip().lower()
        arch = c.run("uname -m").stdout.strip().lower()

        link = f"https://github.com/docker/compose/releases/download/{self.version}/docker-compose-{kernel}-{arch}"  # noqa:501

        c.run(f"curl -sL {link} -o {self.dest}")
        c.run(f"chmod a+x {self.dest}")
        self.log_action("docker-compose", "installed")


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
        rsync_opts: typing.Optional[str] = None,
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
        self.rsync_opts = rsync_opts

        self.rsync_step = transfer.Rsync(
            src_dir_or_file=self.docker_image_path,
            dst_dir=self.dest_dir,
            rsync_opts=self.rsync_opts
        )

    def get_name(self) -> str:
        return f"{super().get_name()}(src={self.docker_image_path}, dst={self.dest_dir})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator("systemctl"),
            validators.CommandRequiredValidator("docker"),
            *self.rsync_step.get_validators(),
        ]

    def run(self, c: Connection) -> None:
        image_file_name = os.path.basename(self.docker_image_path)
        systemd.Start("docker").run(c=c)
        self.rsync_step.run(c)
        c.run(f"cd {self.dest_dir}; docker load -i {image_file_name}")

        if self.rm_after_load:
            c.run(f"rm -rf {self.dest_dir}{image_file_name}")
