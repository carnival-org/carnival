import sys


if not sys.warnoptions:
    import warnings
    warnings.filterwarnings(
        action='default',
        module=r'carnival.*'
    )
