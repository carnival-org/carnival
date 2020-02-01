from carnival import utils, Host, global_context


def test_log(capsys):
    global_context.set_context(Host("local"))
    utils.log("Hellotest")

    captured = capsys.readouterr()
    assert captured.out == "💃💃💃 local> Hellotest\n"
