# Carnival
[![Test](https://github.com/a1fred/carnival/workflows/Test/badge.svg?branch=master)](https://github.com/a1fred/carnival/actions)
[![PyPI version](https://badge.fury.io/py/carnival.svg)](https://badge.fury.io/py/carnival)
[![PyPI](https://img.shields.io/pypi/pyversions/carnival.svg)](https://pypi.python.org/pypi/carnival)

Software provisioning tool, built on top of [Fabric](http://www.fabfile.org/)

* Runs on MacOs and Linux
* Tested automation on Ubuntu and CentOS

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
  -d, --dry_run    Simulate run
  --help           Show this message and exit.
```

### Competion
* for *Bash*: place `eval "$(_CARNIVAL_COMPLETE=source carnival)"` in .bashrc
* for *ZSH*: place `eval "$(_CARNIVAL_COMPLETE=source_zsh carnival)"` in .zshrc

## Quick example
`carnival_file.py` - entry point for carnival cli

Lets create one.
```python
from carnival import Step, Host, Task, cmd

class Deploy(Task):
    def run(self):
        self.step(
            DeployFrontend(),
            Host("1.2.3.5", ssh_user="root", can="context", additional="give"),
        )
    
        self.step(
            DeployFrontend(),
            [
                Host("root@1.2.3.6", can="give", additional="context"),
                Host("root@1.2.3.7", can="context", additional="give"),
            ]
        )


class DeployFrontend(Step):
    def run(self, can, additional, **kwargs):
        cmd.apt.install_multiple("htop", "nginx")
        cmd.systemd.enable("nginx", start_now=True)


class DeployBackend(Step):
    def run(self, can, additional, **kwargs):
        cmd.apt.install_multiple("htop")
        cmd.docker.install_ce_ubuntu()
        cmd.docker.install_compose()
```

Run
```
$  python3 -m carnival deploy
💃💃💃 Runing ⛏frontend at 🖥 1.2.3.4
...
💃💃💃 Runing ⛏frontend at 🖥 1.2.3.5
...
```


## Develop
### Run tests
```bash
$ make dev  # Run docker containers for testing
$ make test_deps  # Install test dependencies
$ make test  # run static analyzers and tests
$ make qs  # Run static analyzers only
$ make nodev  # Stop docker containers
```

### Run carnival from dev env
```bash
$ python3 -m carnival --help
```
