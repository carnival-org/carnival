import typing

if typing.TYPE_CHECKING:
    from carnival import Host


RoleBaseT = typing.TypeVar("RoleBaseT", bound="RoleBase")


class RoleBase:
    """
    Хост, доступная из инстанса роли
    """

    def __init__(self, host: "Host") -> None:
        self.host = host


class Role(RoleBase):
    """
    Роль для нескольких хостов
    """

    @classmethod
    def get_hostroles(cls: typing.Type[RoleBaseT]) -> typing.List["RoleBaseT"]:
        hostroles: typing.List[RoleBaseT] = []

        for host in role_repository.get(cls):
            hostroles.append(cls(host))

        return hostroles


class SingleHostRole(Role):
    """
    Роль для одного хоста
    """

    @classmethod
    def get_hostrole(cls: typing.Type[RoleBaseT]) -> RoleBaseT:
        from carnival.utils import get_class_full_name

        hosts = role_repository.get(cls)
        if len(hosts) != 1:
            raise ValueError(f"Role {get_class_full_name(cls)} must be singe host, but {hosts} already binded")

        return cls(host=list(hosts)[0])


class _RoleRepository:
    def __init__(self) -> None:
        self._rolehosts: typing.Dict[typing.Type[RoleBase], typing.Set["Host"]] = {}

    def items(self) -> typing.Iterable[typing.Tuple[typing.Type[RoleBase], typing.Set["Host"]]]:
        return self._rolehosts.items()

    def add(self, host: "Host", roles: typing.List[typing.Type[RoleBase]]) -> None:
        from carnival.utils import get_class_full_name

        global _rolehosts
        for role in roles:
            if isinstance(role, SingleHostRole):
                hosts = self.get(role)
                if hosts:
                    raise ValueError(
                        f"Cannot bind {host} to single host role {get_class_full_name(role)}, {hosts} already binded"
                    )

            self._rolehosts.setdefault(role, set())
            self._rolehosts[role].add(host)

    def get(self, role: typing.Type[RoleBase]) -> typing.Set["Host"]:
        return self._rolehosts.get(role, set())


role_repository = _RoleRepository()


__all__ = (
    'Role',
    'SingleHostRole',
    'role_repository',
)
