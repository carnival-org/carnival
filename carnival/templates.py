import os
from typing import Any

from jinja2 import (ChoiceLoader, Environment, FileSystemLoader, PackageLoader,
                    PrefixLoader)

from carnival import connection
from carnival.plugins import discover_plugins

"""
Initialize loader on current working dir and plugin modules
"""
j2_env = Environment(loader=ChoiceLoader([
    FileSystemLoader(os.getcwd()),
    PrefixLoader({x: PackageLoader(x, package_path="") for x in discover_plugins().keys()}),
]))


def render(template_path: str, **context: Any) -> str:
    """
    Отрендерить jinja2-шаблон в строку

    :param template_path: относительный путь до шаблона, ищется в текущей папке проекта и в папках плагинов
    :param context: контекст шаблона
    """
    template = j2_env.get_template(template_path)
    return template.render(
        conn=connection.conn,
        connected_host=connection.host,
        host_context=connection,
        **context,
    )
