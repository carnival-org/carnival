from carnival import Task


class Help(Task):
    """
    Показать список доступных задач
    """
    module_name = ""

    def run(self):
        from carnival.cli import task_types
        task_list = list(task_types.keys())
        task_list.sort()

        for task in task_list:
            print(f" * {task}")
