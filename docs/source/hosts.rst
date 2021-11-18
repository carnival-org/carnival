###################
Оборудование (Host)
###################

SSH
======
.. autoclass:: carnival.host.SSHHost()
    :special-members: __init__, connect
    :members:

.. autoclass:: carnival.host.SSHConnection()
    :members: run

Локальный хост
================
.. autoclass:: carnival.host.LocalHost()
    :special-members: __init__, connect
    :members:

.. autoclass:: carnival.host.LocalConnection()
    :members: run


Результат выполнения команд
=============================

.. autoclass:: carnival.host.results.ResultPromise()
    :members:

.. autoclass:: carnival.host.results.Result()
    :members:
