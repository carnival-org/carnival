import typing
import ipaddress
import socket
import abc

from .connection import Connection


class Host:
    addr: str = ""
    """
    Адрес хоста
    """

    def __init__(self, use_sudo: bool = False):
        """
        :param use_sudo: использовать sudo для выполнения команд
        """
        self.use_sudo = use_sudo

    @property
    def ip(self) -> str:
        # Maybe self.addr is ip?
        try:
            ip_obj: typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address] = ipaddress.ip_address(self.addr)
            return ip_obj.__str__()
        except ValueError:
            # Not ip
            pass

        # Maybe hostname?
        try:
            return socket.gethostbyname(self.addr)
        except socket.gaierror:
            # No ;(
            pass

        # TODO: maybe addr is ~/.ssh/config section?

        raise ValueError("cant get host ip")

    @abc.abstractmethod
    def connect(self) -> Connection:
        """
        Создать конект с хостом
        """
        ...

    def __str__(self) -> str:
        return f"🖥 {self.addr}"

    def __hash__(self) -> int:
        return hash(self.addr)

    def __repr__(self) -> str:
        return f"<Host object {self.addr}>"
