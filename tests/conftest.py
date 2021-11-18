import pytest
from carnival.host import localhost, SSHHost
from paramiko.client import WarningPolicy


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: slow tests")
    config.addinivalue_line("markers", "remote: remote connection required")


@pytest.fixture(scope='function')
def suspend_capture(pytestconfig):
    # https://github.com/pytest-dev/pytest/issues/1599
    # Connection local need turn off capturing
    class suspend_guard:
        def __init__(self):
            self.capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

        def __enter__(self) -> None:
            self.capmanager.suspend_global_capture(in_=True)
            pass

        def __exit__(self, _1, _2, _3):
            self.capmanager.resume_global_capture()

    yield suspend_guard()


@pytest.fixture(scope="function")
def local_host():
    return localhost


@pytest.fixture(scope="function")
def ubuntu_ssh_host() -> SSHHost:
    return SSHHost(
        host="127.0.0.1", port=22222,
        ssh_user="root", ssh_password="secret",
        missing_host_key_policy=WarningPolicy
    )


@pytest.fixture(scope="function")
def centos_ssh_host() -> SSHHost:
    return SSHHost(
        host="127.0.0.1", port=22223,
        ssh_user="root", ssh_password="secret",
        missing_host_key_policy=WarningPolicy
    )
