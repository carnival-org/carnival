import typing

from carnival import Step
from carnival import Connection
from carnival.steps import validators


class Update(Step):
    """
    apt-get update
    """

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('apt-get'),
        ]

    def run(self, c: Connection) -> None:
        c.run(
            "apt-get update",
            hide=True,
            env={"DEBIAN_FRONTEND": "noninteractive"},
        )
        self.log_action("apt packages list", "updated")


class GetPackageVersions(Step):
    """
    Получить список доступных версий пакета
    """

    def __init__(self, pkgname: str):
        self.pkgname = pkgname

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('apt-cache'),
        ]

    def run(self, c: Connection) -> typing.List[str]:
        versions = []
        result = c.run(
            f"apt-cache madison {self.pkgname}",
            env={"DEBIAN_FRONTEND": "noninteractive"},
            hide=True,
            warn=True
        )
        if result.ok is False:
            return []

        for line in result.stdout.strip().split("\n"):
            n, ver, r = line.split("|")
            versions.append(ver.strip())
        return versions


class GetInstalledPackageVersion(Step):
    """
    Получить установленную версию пакета

    :return: Версия пакета если установлен, `None` если пакет не установлен
    """

    def __init__(self, pkgname: str):
        self.pkgname = pkgname

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('dpkg'),
        ]

    def run(self, c: Connection) -> typing.Optional[str]:
        result = c.run(
            f"dpkg -l {self.pkgname} | grep '{self.pkgname}'",
            env={"DEBIAN_FRONTEND": "noninteractive"},
            hide=True,
            warn=True,
        )
        if result.ok is False:
            return None

        installed, pkgn, ver, arch, *desc = result.stdout.strip().split("\n")[0].split()
        if installed != 'ii':
            return None

        assert isinstance(ver, str)
        return ver.strip()


class IsPackageInstalled(Step):
    """
    Проверить установлен ли пакет
    Если версия не указана - проверяется любая
    """

    def __init__(self, pkgname: str, version: typing.Optional[str] = None) -> None:
        self.pkgname = pkgname
        self.version = version
        self.get_installed_package_version = GetInstalledPackageVersion(pkgname=self.pkgname)

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return self.get_installed_package_version.get_validators()

    def run(self, c: Connection) -> bool:
        pkgver = self.get_installed_package_version.run(c=c)
        if self.version is None and pkgver is not None:
            return True

        if self.version is not None and pkgver == self.version:
            return True

        return False


class ForceInstall(Step):
    """
    Установить пакет без проверки установлен ли он
    """

    def __init__(self, pkgname: str, version: typing.Optional[str] = None, update: bool = False):
        self.pkgname = pkgname
        self.version = version
        self.update = update

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('apt-get'),
        ]

    def run(self, c: Connection) -> None:
        pkgname = self.pkgname
        if self.version:
            pkgname = f"{self.pkgname}={self.version}"

        if self.update:
            Update().run(c)

        c.run(f"apt-get install -y {pkgname}", env={"DEBIAN_FRONTEND": "noninteractive"})


class Install(Step):
    """
    Установить пакет если он еще не установлен в системе
    """
    def __init__(
        self,
        pkgname: str,
        version: typing.Optional[str] = None,
        update: bool = True,
    ) -> None:
        """
        :param pkgname: название пакета
        :param version: версия
        :param update: запустить apt-get update перед установкой
        """
        self.pkgname = pkgname
        self.version = version
        self.update = update

        self.is_package_installed = IsPackageInstalled(pkgname=self.pkgname, version=self.version)
        self.force_install = ForceInstall(
            pkgname=self.pkgname, version=self.version,
            update=self.update,
        )

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return self.is_package_installed.get_validators() + self.force_install.get_validators()

    def run(self, c: Connection) -> bool:
        if self.is_package_installed.run(c=c):
            if self.version is not None:
                installed_version = GetInstalledPackageVersion(self.pkgname).run(c)
                if installed_version is not None and self.version == installed_version:
                    return False
            else:
                return False
            return False

        ForceInstall(pkgname=self.pkgname, version=self.version, update=self.update).run(c=c)
        self.log_action(self.pkgname, "installed")
        return True


class InstallMultiple(Step):
    """
    Установить несколько пакетов, если они не установлены
    """

    def __init__(self, pkg_names: typing.List[str], update: bool = True) -> None:
        """
        :param pkg_names: список пакетов которые нужно установить
        :param update: запустить apt-get update перед установкой
        """

        self.pkg_names = pkg_names
        self.update = update

    def get_name(self) -> str:
        return f"{super().get_name()}(pkg_names={self.pkg_names})"

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('apt-get'),
        ]

    def run(self, c: Connection) -> bool:
        if all([IsPackageInstalled(x).run(c=c) for x in self.pkg_names]):
            return False

        if self.update:
            Update().run(c)

        for pkg in self.pkg_names:
            Install(pkgname=pkg, update=False).run(c=c)
        return True


class Remove(Step):
    """
    Удалить пакет
    """

    def __init__(self, pkg_names: typing.List[str]) -> None:
        """
        :param pkg_names: список пакетов которые нужно удалить
        """
        self.pkg_names = pkg_names

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.InlineValidator(
                if_err_true_fn=lambda c: not self.pkg_names,
                error_message="'pkg_names' must not be empty",
            ),
            validators.CommandRequiredValidator('apt-get'),
        ]

    def run(self, c: Connection) -> None:
        for pkg in self.pkg_names:
            if IsPackageInstalled(pkg).run(c):
                c.run(
                    f"apt-get remove --auto-remove -y {' '.join(self.pkg_names)}",
                    env={"DEBIAN_FRONTEND": "noninteractive"},
                )
                self.log_action(pkg, "removed")
