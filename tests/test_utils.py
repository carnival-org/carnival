from carnival import utils, LocalHost, global_context


def test_log(capsys):
    with global_context.SetContext(LocalHost()):
        utils.log("Hellotest")

        captured = capsys.readouterr()
        assert captured.out == "💃💃💃 local> Hellotest\n"
