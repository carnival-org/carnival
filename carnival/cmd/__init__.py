"""
Модуль carnival.cmd содержит базовые комманды для взаимодействия с сервером.
Его цель - оставаться простым и помогать в написании шагов (Step).

Для написания сложных сценариев предполагается использовать шаги(Step).

Основные шаги доступны в отдельном репозитории: <https://github.com/carnival-org/carnival-contrib>.
"""

from carnival.cmd import cli, system, systemd, apt, transfer, fs


__all__ = [
    'cli',
    'system',
    'systemd',
    'apt',
    'transfer',
    'fs',
]
