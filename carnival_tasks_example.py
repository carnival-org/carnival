"""
Carnival tasks example file
Run:
CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""

import typing
from dataclasses import dataclass

from carnival.host import localhost, SshHost
from carnival.step import Step, SshStep
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
    local: str
    remote: str


UploadDataProtocolT = typing.TypeVar("UploadDataProtocolT", bound=UploadDataProtocol)


class UploadData(SshStep[UploadDataProtocolT]):  # Step for put file on ssh host (ssh host required)
    def run(self) -> None:
        with self.host.connect() as c:
            cmd.transfer.put(c, self.host.context.local, self.host.context.remote)


#  ## inventory.py
@dataclass
class HostContext:
    disk: str = "/"
    local: str = "/etc/fstab"
    remote: str = "/root/fstab"


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
    hosts: SshHost[HostContext] = [
        SshHost("1.2.3.4", context=HostContext()),
        localhost.with_context(HostContext()),  # type: ignore  # Oops! UploadData cant run on localhost
    ]
    steps = [
        CheckDiskSpace[HostContext],
        UploadData[HostContext],
    ]


class InstallServerBad(SimpleTask[HostContext]):
    hosts = hosts_bad  # type: ignore  # ERROR, wrong context type!
    steps = [
        CheckDiskSpace[HostContext],
        UploadData[HostContext],
    ]
