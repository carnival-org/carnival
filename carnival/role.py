"""
Роль это определенная функция которую можно передать хосту.
У каждой роли может быть несколько задач (Task) для выполнения операций, связанных с ролью
Например деплой, рестарт, просмотр состояния итд

Роли назначаются хостам, одному или нескольким. После назначения все задачи роли будут выполняться
на хостах которым назначена эта роль.

>>> from carnival import Role, Host
>>>
>>>
>>> class NginxRole(Role):
>>>     def __init__(self, host: Host, port: int = 80):
>>>         super().__init__(host)  # Не забываем вызвать конструктор роли, который регистрирует назначение хоста роли
>>>         self.port = port
>>>
>>> # inventory.py
>>>
>>> from carnival import SshHost
>>> my_server = SshHost("1.2.3.4")
>>> NginxRole(my_server, port=8080)  # Назначаем хосту роль
>>>
"""

import typing

if typing.TYPE_CHECKING:
    from carnival import Host


T = typing.TypeVar("T")
RoleT = typing.TypeVar("RoleT", bound="Role")


class Role:
    """
    Объект роли, может быть назначена к нескольким хостам
    """

    def __init__(self, host: "Host") -> None:
        """
        Конструктор роли, назначает хост на роль в carnival

        :param host: хост, назначаемый роли
        """
        self.host = host
        role_repository.add(role=self)

    @classmethod
    def resolve(cls: typing.Type[RoleT]) -> typing.List["RoleT"]:
        """
        Получить список созданных ролей по классу роли
        """
        return role_repository.get(cls)

    @classmethod
    def resolve_host(cls: typing.Type[RoleT], host: "Host") -> RoleT:
        """
        Получить роль по классу роли и хосту
        :param host: хост роли
        :return: Инстанс роли с хостом, если такой зарегистрирован в carnival
        :raise: ValueError - если хост не зарегистрирован в этой роли
        """
        for role in role_repository.get(cls):
            if role.host == host:
                return role
        raise ValueError(f"Role {cls.__name__} with host {host} not registrered")


class SingleRole(Role):
    """
    Роль, которая может быть назначена только одному хосту
    """

    @classmethod
    def resolve_single(cls: typing.Type[RoleT]) -> RoleT:
        """
        Получить роль по классу роли
        """

        from carnival.utils import get_class_full_name

        hostroles = role_repository.get(cls)
        if len(hostroles) != 1:
            raise ValueError(f"Role {get_class_full_name(cls)} must be singe host, but {hostroles} already binded")

        return hostroles[0]


class _RoleRepository:
    def __init__(self) -> None:
        self._rolehosts: typing.List["Role"] = list()

    def items(self) -> typing.List[typing.Tuple[typing.Type[Role], typing.List[Role]]]:
        result: typing.Dict[typing.Type[Role], typing.List[Role]] = dict()
        for role in self._rolehosts:
            result.setdefault(role.__class__, list())
            result[role.__class__].append(role)
        return list(result.items())

    def add(self, role: Role) -> None:
        from carnival.utils import get_class_full_name

        if isinstance(role, SingleRole):
            hostroles = self.get(role.__class__)
            if hostroles:
                role_class_name = get_class_full_name(role.__class__)
                raise ValueError(
                    f"Cannot bind {role} to single host role {role_class_name}, {hostroles} already binded"
                )

        self._rolehosts.append(role)

    def get(self, role_class: typing.Type[RoleT]) -> typing.List[RoleT]:
        result: typing.List[RoleT] = []
        for role in self._rolehosts:
            if isinstance(role, role_class):
                result.append(role)
        return result


role_repository = _RoleRepository()


__all__ = (
    'Role',
    'SingleRole',
    'role_repository',
)
