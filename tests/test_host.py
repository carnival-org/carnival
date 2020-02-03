from carnival import Host


def test_host_create():
    assert Host("root@1.2.3.4:22").host == "1.2.3.4"
    assert Host("1.2.3.4:22").host == "1.2.3.4"
    assert Host("1.2.3.4").host == "1.2.3.4"
    assert Host("abc.example:22").host == "abc.example"
    assert Host("user@abc.example:22").host == "abc.example"

    assert Host("local").is_connection_local() is True
    assert Host("localhost").is_connection_local() is True
    assert Host("user@localhost").is_connection_local() is True

    assert Host("1.2.3.4").is_connection_local() is False
    assert Host("root@1.2.3.4").is_connection_local() is False
    assert Host("root@example.com").is_connection_local() is False

    #  TODO test connection


def test_host_hash():
    h1 = Host("1.2.3.4")
    h2 = Host("1.2.3.4")

    assert h1.__hash__() == h2.__hash__()
