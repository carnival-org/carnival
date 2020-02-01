import pytest

from carnival import Step


@pytest.fixture(scope="function")
def noop_step() -> Step:
    class NoopStep(Step):
        def run(self):
            pass

    return NoopStep()
