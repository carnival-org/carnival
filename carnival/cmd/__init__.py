"""
Модуль carnival.cmd содержит базовые команды для взаимодействия с сервером.
Его цель - оставаться простым и помогать в написании шагов (Step).

Для написания сложных сценариев предполагается использовать шаги(Step).

Основные шаги доступны в отдельном репозитории: <https://github.com/carnival-org/carnival-contrib>.
"""

from carnival.cmd import cli, system, transfer, fs


__all__ = [
    'cli',
    'system',
    'transfer',
    'fs',
]
