from carnival.hosts.base.host import Host
from .connection import LocalConnection


class LocalHost(Host):
    """
    Локальный хост, работает по локальному терминалу
    """

    addr: str = "localhost"
    """
    Адрес хоста, всегда `localhost`
    """

    def connect(self) -> LocalConnection:
        return LocalConnection(host=self)


localhost = LocalHost()
localhost_connection = localhost.connect().__enter__()
