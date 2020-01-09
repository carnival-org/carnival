from typing import Any, Dict

from fabric import Connection

from carnival.core.tasks import Tasks


# Global context vars -----------------
# noinspection PyTypeChecker
conn: Connection = None
host_context = None
secrets: Dict[str, Any] = {}
tasks: Tasks = Tasks()


__all__ = [
    'conn',
    'host_context',
    'secrets',
    'tasks',
]
