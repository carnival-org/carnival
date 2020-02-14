from carnival import internal_tasks


def test_help(capsys):
    internal_tasks.Help(False).run()
