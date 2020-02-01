# Overview

## Docs index
* [step](1%20-%20step.md)
* [commands](2%20-%20commands.md)
* [secrets](3%20-%20secrets.md)

## Cli
Define task in `carnival_file.py`.  
Then you can run `carnival` task on your inventory.

## Quick example
Define task in `carnival_file.py`.
```python
from carnival import Step, Host, cmd, secrets_manager, Task

secrets_manager.secret("root_password", secrets_manager.FromCli())


class SetupFrontend(Task):
    def run(self, **kwargs):
        self.step(Frontend(), Host("1.2.3.4", packages=["htop", ]))

class Frontend(Step):
    def run(self, packages, secrets):
        cmd.apt.install_multiple(packages)
        cmd.system.set_password('root', secrets['root_password'])
        cmd.docker.install_ce()
        cmd.docker.install_compose()
```

Then run
```bash
$ carnival setup_frontend
...
