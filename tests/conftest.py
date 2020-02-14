from typing import Type

import pytest

from carnival import Step, Host


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: slow tests"
    )


@pytest.fixture(scope="function")
def noop_step_class() -> Type[Step]:
    class NoopStep(Step):
        def run(self):
            pass
    return NoopStep


@pytest.fixture(scope="function")
def noop_step(noop_step_class) -> Step:
    return noop_step_class()


@pytest.fixture(scope="function")
def noop_step_context(noop_step_class) -> Step:
    return noop_step_class(additional="context")


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
    return Host("local")


@pytest.fixture(scope="function")
def ubuntu_ssh_host():
    return Host("127.0.0.1", ssh_user="root", ssh_password="secret", ssh_port=22222)


@pytest.fixture(scope="function")
def centos_ssh_host():
    return Host("127.0.0.1", ssh_user="root", ssh_password="secret", ssh_port=22223)
