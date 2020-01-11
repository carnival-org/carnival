# Overview

## Docs index
* [role](1%20-%20role.md)
* [commands](2%20-%20commands.md)
* [secrets](3%20-%20secrets.md)

## Cli
Define role in `carnival_file.py`.  
Then you can run `carnival` task on your inventory.

## Quick example
Define role in `carnival_file.py`.
```python
from carnival import Role, Host, cmd, secrets, global_context

secrets.secret("root_password", secrets.FromCli())

class Frontend(Role):
    # name is optional, carnival generates if not given
    name = "setup_frontend"

    hosts = [
        Host("1.2.3.4", packages=["htop", ])
    ]

    def run(self):
        cmd.apt.install_multiple(global_context.context['packages'])
        cmd.system.set_password('root', global_context.secrets['root_password'])
        cmd.docker.install_ce()
        cmd.docker.install_compose()
```

Then run
```bash
$ carnival setup_frontend
...
