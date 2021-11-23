import pytest

from carnival import LocalHost
from carnival.task import _underscore, Task, SimpleTask


def test_underscore():
    assert _underscore("TestKlass") == 'test_klass'


def test_task_name():
    t: Task

    class DryTask(Task):
        def run(self) -> None:
            pass

    t = DryTask()
    assert t.get_name() == "dry_task"

    class DryNameTask(Task):
        name = "nametask"

        def run(self) -> None:
            pass

    t = DryNameTask()
    assert t.get_name() == "nametask"


def test_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        Task().run()  # type: ignore

    class DryTask(Task):
        def run(self):
            self.step([noop_step, ], [LocalHost(), ])
    t = DryTask()

    t.run()
    spy.assert_called()


def test_simple_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        Task().run()  # type: ignore

    class DryTask(SimpleTask):
        hosts = [LocalHost(), ]
        steps = [noop_step, ]
    t = DryTask()

    t.run()
    spy.assert_called()
