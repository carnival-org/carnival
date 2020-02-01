# Step
Role is group of given commands.

```python
from carnival import Step, cmd


class Frontend(Step):
    def run(self, **kwargs):
        cmd.apt.install_multiple("htop")
        cmd.docker.install_ce()
        cmd.docker.install_compose()
```
