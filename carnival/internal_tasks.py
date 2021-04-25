from carnival import Task


class Help(Task):
    """
    Показать список доступных задач
    """
    module_name = ""
    help = "List available commands and help"

    def run(self) -> None:
        from carnival.cli import task_types

        task_list = list(task_types.keys())
        task_list.sort()

        ralign = max([len(x) for x in task_list]) + 4

        for task_name in task_types.keys():
            help_text = task_types[task_name].help
            if help_text:
                print(f" {task_name:<{ralign}} {help_text}")
            else:
                print(f" {task_name}")
