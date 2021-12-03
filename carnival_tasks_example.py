"""
Carnival tasks example file
Run:
TESTSERVER_ADDR=test_server_addr CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""
import typing

import os
from carnival import cmd, TaskBase, SshHost, Step, Task, Connection, Role


class PackagesRole(Role):
    packages = ['htop', "mc"]


my_server_ip = os.getenv("TESTSERVER_ADDR", "1.2.3.4")  # Dynamic ip for testing
my_server = SshHost(my_server_ip, ssh_user="root")

PackagesRole(my_server)  # Bind server to role


class CheckDiskSpace(TaskBase):
    help = "Print server root disk usage"

    def run(self, disk: str = "/") -> None:
        with my_server.connect() as c:
            cmd.cli.run(c, f"df -h {disk}", hide=False)


class InstallStep(Step):
    def __init__(self, packages: typing.List[str], update: bool = True) -> None:
        self.packages = " ".join(packages)
        self.packages = self.packages.strip()
        self.update = update

    def validate(self, c: Connection) -> typing.List[str]:
        errors = []
        if not self.packages:
            errors.append("packages cant be empty!")

        return errors

    def run(self, c: Connection) -> None:
        if self.update:
            cmd.cli.run(c, "apt-get update")

        cmd.cli.run(c, f"apt-get install -y {self.packages}")


class InstallPackages(Task[PackagesRole]):
    help = "Install packages"

    def get_steps(self) -> typing.List[Step]:
        return [
            InstallStep(packages=self.role.packages),
        ]
