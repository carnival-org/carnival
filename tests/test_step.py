import pytest

from carnival import Step, localhost_connection


def test_step_abc(mocker):
    spy = mocker.spy(Step, 'run')
    with pytest.raises(NotImplementedError):
        Step().run(localhost_connection)  # type: ignore
    spy.assert_called_once()

    spy = mocker.spy(Step, 'validate')
    Step().validate(localhost_connection)  # type: ignore
    spy.assert_called_once()
