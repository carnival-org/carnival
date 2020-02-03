import pytest

from carnival import Step, Host


def test_step_abc(mocker):
    spy = mocker.spy(Step, 'run')
    with pytest.raises(NotImplementedError):
        Step(another="context1").run_with_context(Host("local", add="context"))

    spy.assert_called_once()


def test_step_context_overload(mocker):
    class NoopStep(Step):
        def run(self, another=None):
            pass

    # Waiting step context
    noop_step = NoopStep(another="context1")
    spy = mocker.spy(noop_step, 'run')
    noop_step.run_with_context(Host("local", add="context"))
    spy.assert_called_once_with(another='context1')

    # Waiting no context
    noop_step = NoopStep()
    spy = mocker.spy(noop_step, 'run')
    noop_step.run_with_context(Host("local", add="context"))
    spy.assert_called_once_with()

    # Waiting host context
    noop_step = NoopStep()
    spy = mocker.spy(noop_step, 'run')
    noop_step.run_with_context(Host("local", another="host_context"))
    spy.assert_called_once_with(another="host_context")

    # Waiting step and host context, step context overloading step context
    noop_step = NoopStep(another="context1")
    spy = mocker.spy(noop_step, 'run')
    noop_step.run_with_context(Host("local", another="host_context"))
    spy.assert_called_once_with(another="context1")
