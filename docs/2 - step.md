# Step
Step is group of given commands.

```python
from carnival import Step, cmd


class Frontend(Step):
    def run(self, **kwargs):
        cmd.apt.install_multiple("htop")
        cmd.docker.install_ce_ubuntu()
        cmd.docker.install_compose()
```


