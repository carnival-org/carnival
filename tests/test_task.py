import pytest

from carnival.task import _underscore, Task, TypedTask
from carnival.host.local import localhost, LocalConnection, LocalHost


def test_underscore():
    assert _underscore("TestKlass") == 'test_klass'


def test_task_name():
    t: Task

    class DryTask(Task):
        def run(self):
            pass

    t = DryTask()
    assert t.get_name() == "dry_task"

    class DryNameTask(Task):
        name = "nametask"

        def run(self):
            pass

    t = DryNameTask()
    assert t.get_name() == "nametask"


def test_task():
    with pytest.raises(NotImplementedError):
        Task().run()  # type:ignore  # noqa


def test_typed_task(mocker):
    class TT(TypedTask[LocalHost, LocalConnection]):
        hosts = [localhost, ]

        def host_run(self) -> None:
            pass

    spy = mocker.spy(TT, 'host_run')

    t = TT()
    t.run()
    spy.assert_called()
