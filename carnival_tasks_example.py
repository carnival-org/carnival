"""
Carnival tasks example file
Run:
CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""

import typing
from dataclasses import dataclass

from carnival.host import localhost, localhost_connection, SshHost
from carnival.step import Step
from carnival.task import SimpleTask
from carnival import cmd


#  ## step.py file
class DiskContextProtocol(typing.Protocol):
    disk: str


DiskContextProtocolT = typing.TypeVar("DiskContextProtocolT", bound=DiskContextProtocol)


class CheckDiskSpace(Step[DiskContextProtocolT]):  # Step for check disk space on any host
    def run(self) -> None:
        with self.host.connect() as c:
            cmd.cli.run(c, f"df {self.host.context.disk}")


class UploadDataProtocol(typing.Protocol):
    src: str
    dst: str


UploadDataProtocolT = typing.TypeVar("UploadDataProtocolT", bound=UploadDataProtocol)


class UploadData(Step[UploadDataProtocolT]):  # Step for put file on ssh host (ssh host required)
    def run(self) -> None:
        with self.host.connect() as c:
            cmd.transfer.transfer(
                localhost_connection, self.host.context.src,
                c, self.host.context.dst,
            )


#  ## inventory.py
@dataclass
class HostContext:
    disk: str = "/"
    src: str = "/etc/fstab"
    dst: str = "/root/fstab"


@dataclass
class OtherContext:
    other: str


hosts_good = [
    SshHost("1.2.3.4", context=HostContext()),
    localhost.with_context(HostContext()),
]
hosts_bad = [
    SshHost("1.2.3.4", context=HostContext()),
    localhost.with_context(OtherContext(other="other")),
]


#  ## tasks.py
class InstallServer(SimpleTask[HostContext]):
    hosts = [
        SshHost("1.2.3.4", context=HostContext()),
        localhost.with_context(HostContext()),
    ]
    steps = [
        CheckDiskSpace[HostContext],
        UploadData[HostContext],
    ]


class InstallServerBad(SimpleTask[HostContext]):
    hosts = hosts_bad  # type: ignore  # Oops, Incompatible types in assignment
    steps = [
        CheckDiskSpace[HostContext],
        UploadData[HostContext],
    ]
