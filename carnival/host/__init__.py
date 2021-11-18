from typing import Union

from carnival.host.results import Result
from carnival.host.local import localhost, LocalConnection, LocalHost
from carnival.host.ssh import SSHHost, SSHConnection


AnyHost = Union[LocalHost, SSHHost]
AnyConnection = Union[LocalConnection, SSHConnection]


__all__ = [
    'Result',

    'localhost',
    'SSHHost', 'SSHConnection',

    'AnyHost', 'AnyConnection',
]
