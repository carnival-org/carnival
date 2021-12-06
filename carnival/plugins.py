import typing
import importlib
import pkgutil


def discover_plugins() -> typing.Dict[str, typing.Any]:
    """
    Get modules, name starting with carnival_
    """

    discovered_plugins: typing.Dict[str, typing.Any] = {}

    for finder, name, ispkg in pkgutil.iter_modules():
        if name.startswith('carnival_') and name != 'carnival_tasks' and ispkg is False:
            discovered_plugins[name] = importlib.import_module(name)

    return discovered_plugins
