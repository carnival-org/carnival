from carnival import cli


def test_load_tasks_file():
    assert cli.load_tasks_file("not_exists_file123_") == {}

    tasks = cli.load_tasks_file("tests/fixtures/carnival_file_test.py")
    assert len(tasks) == 1
