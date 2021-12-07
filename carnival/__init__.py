import sys
import dotenv
import os
from carnival.hosts.base.host import Host
from carnival.hosts.base.connection import Connection
from carnival.hosts.base.result import Result
from carnival.steps import Step, InlineStep
from carnival.role import Role, SingleRole
from carnival.hosts.local import LocalHost, localhost_connection, localhost
from carnival.hosts.ssh import SshHost
from carnival.task import TaskBase, Task, TaskGroup
from carnival import internal_tasks


if not sys.warnoptions:
    import warnings
    warnings.filterwarnings(
        action='default',
        module=r'carnival.*'
    )


# Load dotenv first
carnival_dotenv = os.getenv("CARNIVAL_DOTENV", '.env')
"""
Поддерживается передача переменных через `.env-файлы`.

Путь до файла `.env-файла`, по умолчанию `.env`,
можно изменить через переменную окружения `CARNIVAL_DOTENV`.
"""

try:
    dotenv.load_dotenv(dotenv_path=carnival_dotenv)
except OSError:
    # dotenv file not found
    pass


__all__ = [
    'Step', 'InlineStep',
    'SshHost', 'LocalHost', 'localhost', 'localhost_connection',
    'Host', 'Connection', 'Result',
    'Role', 'SingleRole',
    'Task', 'TaskGroup', 'TaskBase',
    'internal_tasks',
]
