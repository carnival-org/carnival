import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Carnival'
copyright = '2020, Dmitry Simonov'
author = 'Dmitry Simonov'

extensions = [
    'sphinx.ext.autodoc',
]
autodoc_default_flags = ['members', ]
templates_path = ['_templates']
language = 'ru'
exclude_patterns = []
html_theme = 'alabaster'
html_static_path = ['_static']
