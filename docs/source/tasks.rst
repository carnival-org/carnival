###################
Задача (Task)
###################

.. autoclass:: carnival.Task
    :members: run

Простые задачи
================

.. autoclass:: carnival.SimpleTask
    :undoc-members: hosts, steps
    :exclude-members: run


Встроенные задачи
===================

carnival имеет встроенные задачи для удобства использования

.. automodule:: carnival.internal_tasks
    :undoc-members:
    :members:

Результат выполнения Task.step
=================================

.. autoclass:: carnival.task.TaskResult
    :undoc-members:
    :members:
