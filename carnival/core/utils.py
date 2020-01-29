import importlib.util
import re
import os

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
    return __import__(os.path.splitext(module_path)[0])
