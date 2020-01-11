from jinja2 import Environment, FileSystemLoader

from carnival import global_context


j2_env = Environment(
    loader=FileSystemLoader('./templates')
)


def render(template_path: str) -> str:
    template = j2_env.get_template(template_path)
    return template.render(
        conn=global_context.conn,
        connected_host=global_context.host,
        host_context=global_context,
        secrets=global_context.secrets,
    )
