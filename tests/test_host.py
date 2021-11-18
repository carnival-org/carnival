import pytest
from carnival.host import SSHHost
from carnival.host.local import LocalHost


def test_host_create():
    with pytest.raises(ValueError):
        SSHHost("1.2.3.4:22", ssh_user="root")
        SSHHost("1.2.3.4:22")
        SSHHost("root@1.2.3.4:22")

    assert SSHHost("1.2.3.4").host == "1.2.3.4"
    assert SSHHost("abc.example").host == "abc.example"

    assert LocalHost()

    #  TODO test connection


def test_host_hash():
    h1 = SSHHost("1.2.3.4")
    h2 = SSHHost("1.2.3.4")

    assert h1.__hash__() == h2.__hash__()
