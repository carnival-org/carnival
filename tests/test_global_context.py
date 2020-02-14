from invoke import Context

from carnival import global_context, Host


def test_global_context():
    h = Host("local")
    assert global_context.host is None
    assert global_context.conn is None

    with global_context.SetContext(h):
        assert global_context.host == h
        assert global_context.conn is not None
        assert isinstance(global_context.conn, Context)

    assert global_context.host is None
    assert global_context.conn is None
