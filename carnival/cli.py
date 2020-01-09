import importlib.util
import argparse
from typing import List

from carnival import inv
from carnival.context import tasks
from carnival.core.tasks import Task


def import_file(module_path: str):
    spec = importlib.util.spec_from_file_location(f"carnival.__{module_path}", module_path)
    _module = importlib.util.module_from_spec(spec)
    return spec.loader.exec_module(_module)


def load_tasks_file(tasks_file: str):
    import_file(tasks_file)


def run_tasks(task_name: List[str], tasks_file: str, dry_run: bool):
    load_tasks_file(tasks_file)

    tasks_to_run: List[Task] = []

    for tn in task_name:
        task = tasks.get_task(tn)
        if task is None:
            raise ValueError(f"Task {tn} not exists.")

        tasks_to_run.append(task)

    for task in tasks_to_run:
        hosts = inv.get_by_role(task.roles)

        for host in hosts:
            print(f"💃💃💃 Runing {task} at {host}")

            if not dry_run:
                inv.set_context(host)
                task.run()


def main():
    parser = argparse.ArgumentParser('Carnival')
    parser.add_argument('-f', '--tasks_file', default="carnival_file.py")
    parser.add_argument('-d', '--dry_run', action='store_true')
    parser.add_argument('task_name', nargs='+')
    args = parser.parse_args()

    run_tasks(**vars(args))
