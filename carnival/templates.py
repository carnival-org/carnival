import os
from typing import Any

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    PrefixLoader,
)
from jinja2.runtime import StrictUndefined
from jinja2.exceptions import UndefinedError, TemplateSyntaxError

from carnival.plugins import discover_plugins


def escape_yaml(data: str) -> str:
    """
    Jinja2 фильтр для экранирования строк в yaml

    экранирует `$`
    """
    return data.replace("$", "$$")


"""
Initialize loader on current working dir and plugin modules
"""
j2_env = Environment(
    loader=ChoiceLoader([
        FileSystemLoader(os.getcwd()),
        PrefixLoader({x: PackageLoader(x, package_path="") for x in discover_plugins().keys()}),
    ]),
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)


j2_env.filters['escape_yaml'] = escape_yaml


def render(template_path: str, **context: Any) -> str:
    """
    Отрендерить jinja2-шаблон в строку

    :param template_path: относительный путь до шаблона, ищется в текущей папке проекта и в папках плагинов
    :param context: контекст шаблона
    """
    try:
        template = j2_env.get_template(template_path)
        return template.render(**context)
    except UndefinedError as ex:
        raise UndefinedError(f"Can't render template {template_path} - {ex}") from ex
    except TemplateSyntaxError as ex:
        raise TemplateSyntaxError(
            message=f"Can't render template {template_path}:{ex.lineno} - {ex.message}",
            lineno=ex.lineno,
            filename=ex.filename,
        ) from ex
