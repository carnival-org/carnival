from invoke import Context  # type: ignore

from carnival import connection
from carnival.host import LocalHost


def test_global_context():
    h = LocalHost()
    assert connection.host is None
    assert connection.conn is None

    with connection.SetConnection(h):
        assert connection.host == h
        assert connection.conn is not None
        assert isinstance(connection.conn, Context)

    assert connection.host is None
    assert connection.conn is None
