from carnival import utils, LocalHost, connection


def test_log(capsys):
    with connection.SetConnection(LocalHost()):
        utils.log("Hellotest")

        captured = capsys.readouterr()
        assert captured.out == "💃💃💃 🖥 local> Hellotest\n"
