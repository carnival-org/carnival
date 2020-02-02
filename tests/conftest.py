import pytest

from carnival import Step, Host, global_context


@pytest.fixture(scope="function")
def noop_step() -> Step:
    class NoopStep(Step):
        def run(self):
            pass

    return NoopStep()


@pytest.fixture(scope="function", params=["local", ])
def host_connection(request):
    return Host(request.param)


@pytest.fixture(scope='function')
def suspend_capture(pytestconfig):
    # https://github.com/pytest-dev/pytest/issues/1599
    # Connection local need turn off capturing
    class suspend_guard:
        def __init__(self):
            self.capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

        def __enter__(self):
            self.capmanager.suspend_global_capture(in_=True)
            pass

        def __exit__(self, _1, _2, _3):
            self.capmanager.resume_global_capture()

    yield suspend_guard()


@pytest.fixture(scope="function")
def host_connection_context(host_connection):
    global_context.set_context(host_connection)
