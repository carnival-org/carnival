from carnival.host import SshHost, LocalHost


def test_host_create():
    assert SshHost("1.2.3.4:22", ssh_user="root", context=None).addr == "1.2.3.4"
    assert SshHost("1.2.3.4:22", context=None).addr == "1.2.3.4"
    assert SshHost("1.2.3.4", context=None).addr == "1.2.3.4"
    assert SshHost("abc.example:22", context=None).addr == "abc.example"

    assert LocalHost(context=None)


def test_host_hash():
    h1 = SshHost("1.2.3.4", context=None)
    h2 = SshHost("1.2.3.4", context=None)

    assert h1.__hash__() == h2.__hash__()
