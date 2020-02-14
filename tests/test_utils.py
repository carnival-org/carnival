from carnival import utils, Host, global_context


def test_log(capsys):
    with global_context.SetContext(Host("local")):
        utils.log("Hellotest")

        captured = capsys.readouterr()
        assert captured.out == "💃💃💃 local> Hellotest\n"
