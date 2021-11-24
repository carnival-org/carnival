from carnival import SshHost, LocalHost


def test_host_create():
    assert SshHost("1.2.3.4")
    assert LocalHost()


def test_host_hash():
    h1 = SshHost("1.2.3.4")
    h2 = SshHost("1.2.3.4")

    assert h1.__hash__() == h2.__hash__()
