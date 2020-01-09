# Carnival [WIP]
Software provisioning tool, built on top of [Fabric](http://www.fabfile.org/)

* Easy to use
* Batteries included

# Docs
Documentation available in [docs directory](docs/0%20-%20overview.md)

# Quick example
carnival_file.py - entry point for carnival cli

Lets create one.
```python
from carnival import inv, cmd, task

# Define our inventory
inv.host('frontend', '1.2.3.4', localip="127.0.0.1")
inv.host('frontend', '1.2.3.5', localip="127.0.0.1")


@task(roles=['frontend'])
def initialize():
    cmd.apt.install_multiple('htop', 'httpie')  # Install apt packages
    cmd.docker.install_ce()  # Install docker ce
    cmd.docker.install_compose()  # Install docker-compose
    cmd.systemd.enable("docker", daemon_reload=True, start_now=True)
```

Run
```
$  python3 -m carnival initialize
💃💃💃 Runing ⛏initialize at 🖥 1.2.3.4
...
💃💃💃 Runing ⛏initialize at 🖥 1.2.3.5
...
```
