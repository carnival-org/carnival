"""
Carnival tasks example file
Run:
CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""

import typing
from dataclasses import dataclass

from carnival.host import localhost, localhost_connection, SshHost
from carnival.step import Step
from carnival.task import Task
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
class HostContext2:
    disk: str = "/"
    src: str = "/etc/fstab"
    dst: str = "/root/fstab"


@dataclass
class OtherContext:
    other: str = ""


ssh_hc = SshHost("1.2.3.4", context=HostContext())
ssh_hc2 = SshHost("1.2.3.4", context=HostContext2())
ssh_oc = SshHost("1.2.3.4", context=OtherContext())

local_hc = localhost.with_context(HostContext())
local_hc2 = localhost.with_context(HostContext2())
local_oc = localhost.with_context(OtherContext())


#  ## tasks.py
class InstallServer(Task):
    def run(self) -> None:
        for h in [ssh_hc, local_hc]:
            UploadData(h)

        for h2 in [ssh_hc, local_hc2]:
            UploadData(h2)  # Not working for now ;(

        UploadData(ssh_hc)
        UploadData(ssh_hc2)
        UploadData(ssh_oc)  # type: ignore # Opps! Context is not compatible for step

        CheckDiskSpace(ssh_hc)
        CheckDiskSpace(ssh_hc2)
        CheckDiskSpace(ssh_oc)  # type: ignore # Opps! Context is not compatible for step

        UploadData(local_hc)
        UploadData(local_hc2)
        UploadData(local_oc)  # type: ignore # Opps! Context is not compatible for step

        CheckDiskSpace(local_hc)
        CheckDiskSpace(local_hc2)
        CheckDiskSpace(local_oc)  # type: ignore # Opps! Context is not compatible for step
