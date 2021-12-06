###################
Оборудование (Host)
###################

.. automodule:: carnival.hosts

Локалхост
================

.. autoclass:: carnival.hosts.local.LocalHost()
    :members:
    :special-members: __init__

.. autoclass:: carnival.hosts.local.LocalConnection()
    :show-inheritance:
    :exclude-members: __init__, __new__

SSH
================

.. autoclass:: carnival.hosts.ssh.SshHost()
    :members:
    :special-members: __init__


.. autoclass:: carnival.hosts.ssh.SshConnection()
    :show-inheritance:
    :exclude-members: __init__, __new__


Соединение
===========
.. autoclass:: carnival.hosts.base.Connection()
    :inherited-members:

.. autoclass:: carnival.hosts.base.Result()
    :members:

.. autoclass:: carnival.hosts.base.StatResult()
    :members:
