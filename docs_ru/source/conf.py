import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Carnival'
copyright = '2020, Dmitry Simonov'
author = 'Dmitry Simonov'

release = os.getenv('DOCS_VERSION', None)
assert release, release
print(f"DOCS_VERSION: {release}")

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_markdown_builder',
]
autodoc_default_options = {
    'members': True,
}
templates_path = ['_templates']
language = 'ru'
exclude_patterns = []
html_theme = 'alabaster'
html_static_path = ['_static']
