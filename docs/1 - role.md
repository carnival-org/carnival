# Role
Role is group of hosts with given commands.

You can define your roles in carnival_file.py

```python
from carnival import Role, Host, cmd


class Frontend(Role):
    hosts = [
        Host("1.2.3.4", can="give", additional="context")
    ]

    def run(self):
        cmd.apt.install_multiple("htop")
        cmd.docker.install_ce()
        cmd.docker.install_compose()
```
