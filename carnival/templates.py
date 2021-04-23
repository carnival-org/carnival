import os
from typing import Any

from jinja2 import (ChoiceLoader, Environment, FileSystemLoader, PackageLoader,
                    PrefixLoader)

from carnival import global_context
from carnival.plugins import discover_plugins

"""
Initialize loader on current working dir and plugin modules
"""
j2_env = Environment(loader=ChoiceLoader([
    FileSystemLoader(os.getcwd()),
    PrefixLoader({x: PackageLoader(x, package_path="") for x in discover_plugins().keys()}),
]))


def render(template_path: str, **context: Any) -> str:
    template = j2_env.get_template(template_path)
    return template.render(
        conn=global_context.conn,
        connected_host=global_context.host,
        host_context=global_context,
        **context,
    )
