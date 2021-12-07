"""
Carnival tasks example file
Run:
TESTSERVER_ADDR=test_server_addr CARNIVAL_TASKS_MODULE=carnival_tasks_example poetry run carnival help
"""
import typing

import os
from carnival import SshHost, Task, Role
from carnival.steps import Step
from carnival.contrib.steps import apt


# Define role
class PackagesRole(Role):
    packages = ['htop', "mc"]


# Define host
my_server_ip = os.getenv("TESTSERVER_ADDR", "1.2.3.4")  # Dynamic ip for testing
my_server = SshHost(my_server_ip, user="root")

# Assign host to role
PackagesRole(my_server)


# Create task for role
class InstallPackages(Task[PackagesRole]):
    help = "Install packages"

    def get_steps(self) -> typing.List[Step]:
        return [
            apt.InstallMultiple(self.role.packages)
        ]
