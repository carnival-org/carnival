from carnival.host import SSHHost, LocalHost


def test_host_create():
    assert SSHHost("1.2.3.4")
    assert LocalHost()


def test_host_hash():
    h1 = SSHHost("1.2.3.4")
    h2 = SSHHost("1.2.3.4")

    assert h1.__hash__() == h2.__hash__()
