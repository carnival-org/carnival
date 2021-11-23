"""
Carnival tasks example file
Run:
TESTSERVER_ADDR=test_server_addr CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""
import typing

import os
from carnival import cmd
from carnival.task import Task, SimpleTask
from carnival.host import SSHHost
from carnival.step import Step
from carnival import global_context


my_server_ip = os.getenv("TESTSERVER_ADDR", "1.2.3.4")
my_server = SSHHost(my_server_ip, ssh_user="root", packages=['htop', "mc"])


class CheckDiskSpace(Task):
    help = "Print server root disk usage"

    def run(self) -> None:
        with global_context.SetContext(my_server):
            cmd.cli.run("df -h /", hide=False)


class InstallStep(Step):
    def run(self, packages: typing.List[str]) -> None:
        cmd.apt.install_multiple(*packages)


class InstallPackages(SimpleTask):
    help = "Install packages"

    hosts = [my_server]
    steps = [InstallStep()]
