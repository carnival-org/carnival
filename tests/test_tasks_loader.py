from carnival import tasks_loader


def test_load_tasks_file():
    initial_tasks = tasks_loader.get_tasks_from_runtime("")

    tasks_loader.import_tasks_file("not_exists_file123_", silent=True)
    assert tasks_loader.get_tasks_from_runtime("") == initial_tasks

    tasks_loader.import_tasks_file("testdata.carnival_file_test", silent=False)
    tasks = tasks_loader.get_tasks_from_runtime("")
    assert len(tasks) == len(initial_tasks) + 1
