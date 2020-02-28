from typing import Dict, Any
import importlib
import pkgutil


def discover_plugins() -> Dict[str, Any]:
    """
    Get modules, name starting with carnival_
    """

    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules() if name.startswith('carnival_') and name != 'carnival_tasks'
    }
    return discovered_plugins
