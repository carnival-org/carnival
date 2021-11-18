###################
Задача (Task)
###################

.. autoclass:: carnival.task.Task
    :members: run

Типизированные задачи
=======================
carnival 2 был написан с использованием строгой типизации

.. autoclass:: carnival.task.TypedTask
    :members:

.. autoclass:: carnival.task.SSHTask
    :members:
    :undoc-members: hosts, c, host_run
    :exclude-members: run

Встроенные задачи
===================

carnival имеет встроенные задачи для удобства использования

.. automodule:: carnival.internal_tasks
    :undoc-members:
    :members:
    :exclude-members: module_name, run
