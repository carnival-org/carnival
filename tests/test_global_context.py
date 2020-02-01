from invoke import Context

from carnival import global_context, Host


def test_global_context():
    h = Host("local")
    global_context.set_context(h)
    assert global_context.host == h
    assert global_context.conn is not None
    assert isinstance(global_context.conn, Context)
