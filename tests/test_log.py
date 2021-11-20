from carnival.log import log
from carnival.host import SshHost


def test_log(capsys):
    host = SshHost("1.2.3.4", context=None)
    log(host=host, message="Hellotest")
    captured = capsys.readouterr()
    assert captured.out == "💃💃💃 local> Hellotest\n"
