import sys
import dotenv
import os
from carnival.step import Step, InlineStep
from carnival.hosts.base import Host, Connection, Result
from carnival.role import Role, SingleRole
from carnival.hosts.local import LocalHost, localhost_connection
from carnival.hosts.ssh import SshHost
from carnival.task import TaskBase, Task
from carnival import cmd
from carnival import internal_tasks
from carnival.utils import log


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
    'SshHost', 'LocalHost', 'localhost_connection', 'Host', 'Connection', 'Result',
    'Role', 'SingleRole',
    'TaskBase', 'Task',
    'cmd',
    'log',
    'internal_tasks',
]
