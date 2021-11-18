import os
from typing import Any

from jinja2 import (ChoiceLoader, Environment, FileSystemLoader, PackageLoader,
                    PrefixLoader)

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
    Отрендерить файл шаблона в строку

    :param template_path: путь до файла jinja2, можно использовать относительный путь (от корня проекта)
    :param context: контекст шаблона
    """
    template = j2_env.get_template(template_path)
    return template.render(**context)
