import typing

if typing.TYPE_CHECKING:
    from carnival import Host


T = typing.TypeVar("T")
RoleBaseT = typing.TypeVar("RoleBaseT", bound="RoleBase")


class RoleBase:
    """
    Хост, доступная из инстанса роли
    """

    def __init__(self, host: "Host") -> None:
        self.host = host
        role_repository.add(role=self)


class Role(RoleBase):
    """
    Роль для нескольких хостов
    """

    @classmethod
    def resolve(cls: typing.Type[RoleBaseT]) -> typing.List["RoleBaseT"]:
        return role_repository.get(cls)

    @classmethod
    def resolve_host(cls: typing.Type[RoleBaseT], host: "Host") -> RoleBaseT:
        for role in role_repository.get(cls):
            if role.host == host:
                return role
        raise ValueError("Role {} with host {} not registrered")


class SingleRole(Role):
    """
    Роль для одного хоста
    """

    @classmethod
    def resolve_single(cls: typing.Type[RoleBaseT]) -> RoleBaseT:
        from carnival.utils import get_class_full_name

        hostroles = role_repository.get(cls)
        if len(hostroles) != 1:
            raise ValueError(f"Role {get_class_full_name(cls)} must be singe host, but {hostroles} already binded")

        return hostroles[0]


class _RoleRepository:
    def __init__(self) -> None:
        self._rolehosts: typing.List["RoleBase"] = list()

    def items(self) -> typing.Iterable[typing.Tuple[typing.Type[RoleBase], typing.List[RoleBase]]]:
        result: typing.Dict[typing.Type[RoleBase], typing.List[RoleBase]] = dict()
        for role in self._rolehosts:
            result.setdefault(role.__class__, list())
            result[role.__class__].append(role)
        return list(result.items())

    def add(self, role: RoleBase) -> None:
        from carnival.utils import get_class_full_name

        if isinstance(role, SingleRole):
            hostroles = self.get(role.__class__)
            if hostroles:
                role_class_name = get_class_full_name(role.__class__)
                raise ValueError(
                    f"Cannot bind {role} to single host role {role_class_name}, {hostroles} already binded"
                )

        self._rolehosts.append(role)

    def get(self, role_class: typing.Type[RoleBaseT]) -> typing.List[RoleBaseT]:
        result: typing.List[RoleBaseT] = []
        for role in self._rolehosts:
            if isinstance(role, role_class):
                result.append(role)
        return result


role_repository = _RoleRepository()


# def role_ref(role_class: RoleBaseT, getter: typing.Callable[[RoleBaseT], T]) -> typing.List[T]:
#     resuts: typing.List[T] = []
#     for role in role_repository.get(role_class):
#         resuts.append(getter(role))
#     return resuts


__all__ = (
    'Role',
    'SingleRole',
    'role_repository',
)
