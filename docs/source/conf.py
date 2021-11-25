import os
import sys
import typing
sys.path.insert(0, os.path.abspath('../../'))

project = 'Carnival'
copyright = '2021, Dmitry Simonov'
author = 'Dmitry Simonov'

html_theme_options = {
    "page_width": "1024px",
}

extensions = [
    'sphinx.ext.autodoc',
]
autodoc_mock_imports = [
    'fabric',
    'invoke',
    'jinja2',
    'click',
    'paramiko',
    'dotenv',
]
master_doc = 'index'
autodoc_default_flags = ['members', ]
templates_path = ['_templates']
language = 'ru'
exclude_patterns: typing.List[str] = []
html_theme = 'alabaster'
html_static_path = ['_static']
