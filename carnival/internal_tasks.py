from carnival import TaskBase
from carnival.utils import get_class_full_name


class Help(TaskBase):
    """
    Показать список доступных задач
    """
    module_name = ""
    help = "List available tasks and help"

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
    """
    module_name = ""
    help = "Validate available tasks"

    def run(self) -> None:
        from carnival.cli import task_types

        all_errors = []

        task_list = list(task_types.keys())
        task_list.sort()

        for task_name in task_list:
            all_errors += task_types[task_name](no_validate=False).validate()

        if all_errors:
            for e in all_errors:
                print(f" * {e}")
            return

        print("All tasks are valid.")


class Roles(TaskBase):
    """
    Показать список ролей и хостов
    """
    module_name = ""
    help = "Show all roles and hosts"

    def run(self) -> None:
        from carnival.role import role_repository

        for role, hosts in role_repository.items():
            print(f"{get_class_full_name(role)}: {', '.join([x.addr for x in hosts])}")
