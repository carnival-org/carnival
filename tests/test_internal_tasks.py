from carnival import internal_tasks


def test_help(capsys):
    internal_tasks.Help(True).run()
    internal_tasks.Validate(False).run()
    internal_tasks.Roles(True).run()
