import importlib.util
import re

from carnival import global_context


def run_command(command: str, **kwargs):
    return global_context.conn.run(command, **kwargs)


def underscore(word: str) -> str:
    # https://github.com/jpvanhal/inflection/blob/master/inflection.py
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def import_file(module_path: str):
    spec = importlib.util.spec_from_file_location(f"carnival.__{module_path}", module_path)
    _module = importlib.util.module_from_spec(spec)
    return spec.loader.exec_module(_module)
