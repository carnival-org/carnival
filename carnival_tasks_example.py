"""
Carnival tasks example file
Run:
CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""

import typing
from dataclasses import dataclass

from carnival.host import Host, SshHost, localhost_connection
from carnival.task import Task
from carnival import cmd


# role.py
class Role(typing.Protocol):
    host: Host


#  ## step.py file
class DiskContextProtocol(Role, typing.Protocol):
    disk: str


def check_disk_space(ctx: DiskContextProtocol) -> None:  # Step for check disk space on any host
    with ctx.host.connect() as c:
        cmd.cli.run(c, f"df {ctx.disk}")


class UploadDataProtocol(Role, typing.Protocol):
    src: str
    dst: str


def upload_data(ctx: UploadDataProtocol) -> None:  # Step for put file on ssh host (ssh host required)
    with ctx.host.connect() as c:
        cmd.transfer.transfer(
            localhost_connection, ctx.src,
            c, ctx.dst,
        )


class OtherProtocol(Role, typing.Protocol):
    size: int = 10


def other_step(ctx: None) -> None:
    pass


#  ## inventory.py
@dataclass
class HostContext:
    host: Host
    disk: str = "/"
    src: str = "/etc/fstab"
    dst: str = "/root/fstab"


@dataclass
class HostContext2:
    host: Host
    disk: str = "/"
    src: str = "/etc/fstab"
    dst: str = "/root/fstab"
    ll: int = 1


@dataclass
class OtherContext:
    host: Host
    size: int = 1


ssh_host = SshHost("1.2.3.4")


ssh_hc = HostContext(host=ssh_host)
ssh_hc2 = HostContext2(host=ssh_host)
ssh_oc = OtherContext(host=ssh_host)


#  ## tasks.py
T = typing.TypeVar("T", bound=Role)


class SimpleTask(typing.Generic[T], Task):
    def __init__(
        self,
        role: T,
        steps: typing.List[typing.Callable[[T], None]],
    ) -> None:
        self.role = role
        self.steps = steps

    def run(self) -> None:
        return super().run()


SimpleTask(
    role=ssh_hc,
    steps=[
        upload_data,
        check_disk_space,
        other_step,  # type: ignore # Oops wrong context type
    ]
)
