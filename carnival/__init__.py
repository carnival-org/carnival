from carnival.core.inventory import Inventory
from carnival.tasks import task
from carnival import secrets


inv = Inventory()


__all__ = [
    'task',
    'inv',
    'secrets',
]
