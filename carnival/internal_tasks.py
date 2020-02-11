from carnival import Task


class Help(Task):
    def run(self):
        from carnival.cli import get_tasks
        tasklist = list(get_tasks().keys())
        tasklist.sort()

        for task in tasklist:
            print(f" * {task}")
