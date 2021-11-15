from invoke import Context

from carnival import global_context
from carnival.host import LocalHost


def test_global_context():
    h = LocalHost()
    assert global_context.host is None
    assert global_context.conn is None

    with global_context.SetContext(h):
        assert global_context.host == h
        assert global_context.conn is not None
        assert isinstance(global_context.conn, Context)

    assert global_context.host is None
    assert global_context.conn is None
