# Carnival [WIP]
[![PyPI version](https://badge.fury.io/py/carnival.svg)](https://badge.fury.io/py/carnival)
[![PyPI](https://img.shields.io/pypi/pyversions/carnival.svg)](https://pypi.python.org/pypi/carnival)

Software provisioning tool, built on top of [Fabric](http://www.fabfile.org/)

* Easy to use
* Batteries included

## Install
```bash
$ pip3 install carnival
```

## Docs
Documentation available in [docs directory](docs/0%20-%20overview.md)

## Cli
### Usage
```bash
$ carnival --help
Usage: carnival [OPTIONS] [deploy_frontend|deploy_backend]...

Options:
  -d, --dry_run
  --help         Show this message and exit.
```

### Competion
* for *Bash*: place `eval "$(_CARNIVAL_COMPLETE=source carnival)"` in .bashrc
* for *ZSH*: place `eval "$(_CARNIVAL_COMPLETE=source_zsh carnival)"` in .zshrc

## Quick example
`carnival_file.py` - entry point for carnival cli

Lets create one.
```python
from carnival import Role, Host, cmd


class DeployFrontend(Role):
    hosts = [
        Host("1.2.3.4", can="give", additional="context"),
        Host("1.2.3.5", can="context", additional="give"),
    ]

    def run(self):
        cmd.apt.install_multiple("htop", "nginx")
        cmd.systemd.enable("nginx", start_now=True)


class DeployBackend(Role):
    hosts = [
        Host("1.2.3.6", can="give", additional="context"),
        Host("1.2.3.7", can="context", additional="give"),
    ]

    def run(self):
        cmd.apt.install_multiple("htop")
        cmd.docker.install_ce()
        cmd.docker.install_compose()
```

Run
```
$  python3 -m carnival deploy_frontend
💃💃💃 Runing ⛏frontend at 🖥 1.2.3.4
...
💃💃💃 Runing ⛏frontend at 🖥 1.2.3.5
...
```
