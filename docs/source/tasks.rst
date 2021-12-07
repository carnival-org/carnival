###################
Задача (Task)
###################

.. autoclass:: carnival.TaskBase()
    :members:
    :exclude-members: __init__

Задачи ролей
================

.. autoclass:: carnival.Task()
    :members: get_steps, role
    :show-inheritance:
    :exclude-members: __init__, __new__

Группа задач
=============

.. autoclass:: carnival.TaskGroup()
    :members: tasks
    :show-inheritance:
    :exclude-members: __init__, __new__

Встроенные задачи
===================

carnival имеет встроенные задачи для удобства использования

.. automodule:: carnival.internal_tasks
    :members:
    :exclude-members: run, get_validation_errors
