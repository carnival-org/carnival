from carnival import utils, LocalHost


def test_log(capsys):
    utils.log("Hellotest", host=LocalHost())
    captured = capsys.readouterr()
    assert captured.out == "💃💃💃 🖥 local> Hellotest\n"
