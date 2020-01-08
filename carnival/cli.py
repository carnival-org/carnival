import importlib.util
import argparse
from carnival.context import tasks


def load_tasks_file(tasks_file: str):
    spec = importlib.util.spec_from_file_location("carnival._tasks__file", tasks_file)
    _tasks_file_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_tasks_file_module)


def runtask(task_name: str, tasks_file: str):
    load_tasks_file(tasks_file)
    tasks.run_task(task_name)


def main():
    parser = argparse.ArgumentParser('Carnival')
    parser.add_argument('-f', '--tasks_file', default="carnival_file.py")
    parser.add_argument('task_name')
    args = parser.parse_args()

    runtask(**vars(args))
