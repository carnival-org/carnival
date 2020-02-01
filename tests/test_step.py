from carnival import Task, Host


def test_task(noop_step, mocker):
    spy = mocker.spy(noop_step, 'run')

    class DryTask(Task):
        def run(self):
            self.step(noop_step, Host("local"))
            self.step([noop_step, ], [Host("local"), ])
    t = DryTask(False)

    t.run()
    spy.assert_called()
