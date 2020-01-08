from fabric import Connection

from carnival.core.tasks import Tasks


# Global context vars -----------------
# noinspection PyTypeChecker
conn: Connection = None  # type: ignore
conn_context = None

tasks: Tasks = Tasks()
