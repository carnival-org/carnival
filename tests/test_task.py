import pytest

from carnival import LocalHost
from carnival.task import _underscore, TaskBase, StepsTask


def test_underscore():
    assert _underscore("TestKlass") == 'test_klass'


def test_task_name():
    t: TaskBase

    class DryTask(TaskBase):
        def run(self) -> None:
            pass

    t = DryTask()
    assert t.get_name() == "dry_task"

    class DryNameTask(TaskBase):
        name = "nametask"

        def run(self) -> None:
            pass

    t = DryNameTask()
    assert t.get_name() == "nametask"


def test_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        TaskBase().run()  # type: ignore

    spy.assert_not_called()


def test_simple_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        TaskBase().run()  # type: ignore

    class DryTask(StepsTask):
        hosts = [LocalHost(), ]
        steps = [noop_step, ]
    t = DryTask()

    t.run()
    spy.assert_called()
