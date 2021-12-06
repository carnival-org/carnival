import typing

from colorama import Style as S, Fore as F  # type: ignore

from carnival import Step
from carnival import Connection
from carnival.steps import validators


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
        result = c.run(f"DEBIAN_FRONTEND=noninteractive apt-cache madison {self.pkgname}", hide=True, warn=True)
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
        """
        :return: Версия пакета если установлен, `None` если пакет не установлен
        """
        result = c.run(
            f"DEBIAN_FRONTEND=noninteractive dpkg -l {self.pkgname} | grep '{self.pkgname}'",
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
        """
        Проверить установлен ли пакет
        Если версия не указана - проверяется любая
        """

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

    def __init__(self, pkgname: str, version: typing.Optional[str] = None, update: bool = False, hide: bool = False):
        self.pkgname = pkgname
        self.version = version
        self.update = update
        self.hide = hide

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('apt-get'),
        ]

    def run(self, c: Connection) -> None:
        pkgname = self.pkgname
        if self.version:
            pkgname = f"{self.pkgname}={self.version}"

        if self.update:
            c.run("DEBIAN_FRONTEND=noninteractive sudo apt-get update", hide=self.hide)

        c.run(f"DEBIAN_FRONTEND=noninteractive sudo apt-get install -y {pkgname}", hide=self.hide)


class Install(Step):
    """
    Установить пакет если он еще не установлен в системе
    """
    def __init__(
        self,
        pkgname: str,
        version: typing.Optional[str] = None,
        update: bool = True,
        hide: bool = False,
    ) -> None:
        """
        :param pkgname: название пакета
        :param version: версия
        :param update: запустить apt-get update перед установкой
        :param hide: скрыть вывод этапов
        """
        self.pkgname = pkgname
        self.version = version
        self.update = update
        self.hide = hide

        self.is_package_installed = IsPackageInstalled(pkgname=self.pkgname, version=self.version)
        self.force_install = ForceInstall(
            pkgname=self.pkgname, version=self.version,
            update=self.update, hide=self.hide
        )

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return self.is_package_installed.get_validators() + self.force_install.get_validators()

    def run(self, c: Connection) -> bool:
        """
        :return: `True` если пакет был установлен, `False` если пакет уже был установлен ранее
        """
        if self.is_package_installed.run(c=c):
            if self.version is not None:
                installed_version = GetInstalledPackageVersion(self.pkgname).run(c)
                if installed_version is not None and self.version == installed_version:
                    return False
            else:
                return False
            return False

        ForceInstall(pkgname=self.pkgname, version=self.version, update=self.update, hide=self.hide).run(c=c)
        print(f"{S.BRIGHT}{self.pkgname}{S.RESET_ALL}: {F.YELLOW}installed{F.RESET}")
        return True


class InstallMultiple(Step):
    """
    Установить несколько пакетов, если они не установлены
    """

    def __init__(self, pkg_names: typing.List[str], update: bool = True, hide: bool = False) -> None:
        """
        :param pkg_names: список пакетов которые нужно установить
        :param update: запустить apt-get update перед установкой
        :param hide: скрыть вывод этапов
        """

        self.pkg_names = pkg_names
        self.update = update
        self.hide = hide

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.CommandRequiredValidator('apt-get'),
        ]

    def run(self, c: Connection) -> bool:
        """
        :return: `True` если хотя бы один пакет был установлен, `False` если все пакеты уже были установлен ранее
        """
        if all([IsPackageInstalled(x).run(c=c) for x in self.pkg_names]):
            return False

        if self.update:
            c.run("DEBIAN_FRONTEND=noninteractive sudo apt-get update", hide=self.hide)

        for pkg in self.pkg_names:
            Install(pkgname=pkg, update=False, hide=self.hide).run(c=c)
        return True


class Remove(Step):
    """
    Удалить пакет
    """

    def __init__(self, pkg_names: typing.List[str], hide: bool = False) -> None:
        """
        :param pkg_names: список пакетов которые нужно удалить
        :param hide: скрыть вывод этапов
        """
        self.pkg_names = pkg_names
        self.hide = hide

    def get_validators(self) -> typing.List[validators.StepValidatorBase]:
        return [
            validators.InlineValidator(
                if_err_true_fn=lambda c: not self.pkg_names,
                error_message="'pkg_names' must not be empty",
            ),
            validators.CommandRequiredValidator('apt-get'),
        ]

    def run(self, c: Connection) -> None:
        c.run(
            f"DEBIAN_FRONTEND=noninteractive sudo apt-get remove --auto-remove -y {' '.join(self.pkg_names)}",
            hide=self.hide
        )
