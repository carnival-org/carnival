import pytest

from carnival import Step, LocalHost


def test_step_abc(mocker):
    spy = mocker.spy(Step, 'run')
    with pytest.raises(NotImplementedError):
        Step().run(LocalHost())  # type: ignore
    spy.assert_called_once()

    spy = mocker.spy(Step, 'validate')
    Step().validate(LocalHost())  # type: ignore
    spy.assert_called_once()
