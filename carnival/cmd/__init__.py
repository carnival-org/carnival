"""
Модуль carnival.cmd содержит минимальные комманды для взаимодействия с сервером.
Расширенные команды доступны в отдельном репозитории: <https://github.com/carnival-org/carnival-contrib>.
"""

from carnival.cmd import cli, transfer


__all__ = [
    'cli',
    'transfer',
]
