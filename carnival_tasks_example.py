"""
Carnival tasks example file

Run:
CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""

import os
from carnival import cmd
from carnival.task import Task
from carnival.task import TypedTask
from carnival.host import SSHHost, SSHConnection


my_server_ip = os.getenv("TESTSERVERIP", "1.2.3.4")
my_server = SSHHost(my_server_ip, ssh_user="root")


class Test(Task):
    def run(self) -> None:
        with my_server.connect() as c:
            cmd.cli.run(c, "df -h /", hide=False)
            cmd.transfer.rsync(my_server, ".", "/tmp/carnival/")


class FrontendHost(SSHHost):
    packages = ['htop', "mc"]


class Deploy(TypedTask[FrontendHost, SSHConnection]):
    hosts = [
        FrontendHost(my_server_ip),
    ]

    def host_run(self) -> None:
        cmd.cli.run(self.c, "apt update")
        cmd.cli.run(self.c, "apt install -y %s" % " ".join(self.host.packages))
