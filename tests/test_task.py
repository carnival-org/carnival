import pytest

from carnival import Host
from carnival.task import _underscore, Task, SimpleTask


def test_underscore():
    assert _underscore("TestKlass") == 'test_klass'


def test_task_name():
    class DryTask(Task):
        pass

    t = DryTask(True)
    assert t.get_name() == "dry_task"

    class DryNameTask(Task):
        name = "nametask"

    t = DryNameTask(True)
    assert t.get_name() == "nametask"


def test_task_dry_run(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    class DryTask(Task):
        def run(self):
            self.step(noop_step, Host("local"))
    t = DryTask(True)

    t.run()
    spy.assert_not_called()


def test_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        Task(False).run()

    class DryTask(Task):
        def run(self):
            self.step(noop_step, Host("local"))
            self.step([noop_step, ], [Host("local"), ])
    t = DryTask(False)

    t.run()
    spy.assert_called()


def test_simple_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    with pytest.raises(NotImplementedError):
        Task(False).run()

    class DryTask(SimpleTask):
        hosts = [Host("local"), ]
        steps = [noop_step, ]
    t = DryTask(False)

    t.run()
    spy.assert_called()
