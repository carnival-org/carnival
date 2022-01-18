import typing

from carnival import TaskBase
from carnival.hosts.base.host import Host
from carnival.utils import get_class_full_name


class Help(TaskBase):
    """
    Показать список доступных задач

        $ carnival help
    """
    module_name = ""
    help = "List available tasks and help"

    def get_validation_errors(self) -> typing.List[str]:
        return []

    def run(self) -> None:
        from carnival.cli import task_types

        task_list = list(task_types.keys())

        ralign = 4
        if task_list:
            ralign += max([len(x) for x in task_list])

        for task_name in task_list:
            help_text = task_types[task_name].help
            if help_text:
                print(f" {task_name:<{ralign}} {help_text}")
            else:
                print(f" {task_name}")


class Validate(TaskBase):
    """
    Запустить валидацию доступых задач и напечатать список ошибок

        $ carnival validate
    """
    module_name = ""
    help = "Validate available tasks"

    def get_validation_errors(self) -> typing.List[str]:
        return []

    def run(self) -> None:
        from carnival.cli import task_types

        task_list = list(task_types.keys())
        task_list.sort()

        for task_name in task_list:
            task_types[task_name](no_validate=False).validate()


class Roles(TaskBase):
    """
    Показать список хостов по ролям

        $ carnival roles
    """
    module_name = ""
    help = "Show all hosts by role"

    def get_validation_errors(self) -> typing.List[str]:
        return []

    def run(self) -> None:
        from carnival.role import role_repository

        for role, hosts in role_repository.items():
            print(f"{get_class_full_name(role)}: {', '.join([x.host.addr for x in hosts])}")


class Hosts(TaskBase):
    """
    Показать список ролей по хостам

        $ carnival hosts
    """
    module_name = ""
    help = "Show all roles by host"

    def get_validation_errors(self) -> typing.List[str]:
        return []

    def run(self) -> None:
        from carnival.role import role_repository

        hosts: typing.Dict[Host, typing.List[str]] = {}

        for role, rolehosts in role_repository.items():
            for rolehost in rolehosts:
                if rolehost.host in hosts:
                    hosts[rolehost.host].append(get_class_full_name(role))
                else:
                    hosts[rolehost.host] = [get_class_full_name(role), ]

        for host, roles in hosts.items():
            print(f"{host} roles ({len(roles)} total):")
            for rolename in roles:
                print(f"    - {rolename}")
