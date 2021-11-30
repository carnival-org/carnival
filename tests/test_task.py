import pytest
import typing

from carnival import LocalHost, Step
from carnival.role import Role
from carnival.task import _underscore, TaskBase, Task


def test_underscore():
    assert _underscore("TestKlass") == 'test_klass'


def test_task_name():
    t: TaskBase

    class DryTask(TaskBase):
        def run(self) -> None:
            pass

    t = DryTask(True)
    assert t.get_name() == "dry_task"

    class DryNameTask(TaskBase):
        name = "nametask"

        def run(self) -> None:
            pass

    t = DryNameTask(True)
    assert t.get_name() == "nametask"


def test_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        TaskBase(False).run()  # type: ignore

    spy.assert_not_called()


def test_simple_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        TaskBase(False).run()  # type: ignore

    class DryTask(Task[Role]):
        hosts = [LocalHost(), ]

        def get_steps(self) -> typing.List[Step]:
            return [noop_step, ]
    t = DryTask(True)

    t.run()
    spy.assert_called()
