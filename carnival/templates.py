import os

from jinja2 import Environment, FileSystemLoader

from carnival import global_context
from carnival.secrets_manager import secrets_storage

j2_env = Environment(
    loader=FileSystemLoader(os.getcwd())
)


def render(template_path: str, **context) -> str:
    template = j2_env.get_template(template_path)
    return template.render(
        conn=global_context.conn,
        connected_host=global_context.host,
        host_context=global_context,
        secrets=secrets_storage,
        **context,
    )
