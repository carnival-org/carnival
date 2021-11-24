from typing import Type

import pytest
from carnival import Step, SshHost, LocalHost
from paramiko.client import WarningPolicy


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: slow tests")
    config.addinivalue_line("markers", "remote: remote connection required")


@pytest.fixture(scope="function")
def noop_step_class() -> Type[Step]:
    class NoopStep(Step):
        def run(self, c):
            pass
    return NoopStep


@pytest.fixture(scope="function")
def noop_step(noop_step_class: Type[Step]) -> Step:
    return noop_step_class()


@pytest.fixture(scope='function')
def suspend_capture(pytestconfig):
    # https://github.com/pytest-dev/pytest/issues/1599
    # Connection local need turn off capturing
    class suspend_guard:
        def __init__(self):
            self.capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

        def __enter__(self):
            self.capmanager.suspend_global_capture(in_=True)
            pass

        def __exit__(self, _1, _2, _3):
            self.capmanager.resume_global_capture()

    yield suspend_guard()


@pytest.fixture(scope="function")
def local_host():
    return LocalHost()


@pytest.fixture(scope="function")
def ubuntu_ssh_host():
    return SshHost(
        "127.0.0.1",
        ssh_user="root", ssh_password="secret", ssh_port=22222,
        missing_host_key_policy=WarningPolicy
    )


@pytest.fixture(scope="function")
def centos_ssh_host():
    return SshHost(
        "127.0.0.1",
        ssh_user="root", ssh_password="secret", ssh_port=22223,
        missing_host_key_policy=WarningPolicy
    )
