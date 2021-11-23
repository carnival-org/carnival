from carnival import TaskBase


class Help(TaskBase):
    """
    Показать список доступных задач
    """
    module_name = ""
    help = "List available tasks and help"

    def run(self) -> None:
        from carnival.cli import task_types

        task_list = list(task_types.keys())
        task_list.sort()

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
            all_errors += task_types[task_name]().validate()

        if all_errors:
            for e in all_errors:
                print(f" * {e}")
            return

        print("All tasks are valid.")
