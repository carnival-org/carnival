# Carnival
[![Tests](https://github.com/carnival-org/carnival/workflows/Tests/badge.svg?branch=master)](https://github.com/carnival-org/carnival/actions?query=branch%3Amaster)
[![PyPI version](https://badge.fury.io/py/carnival.svg)](https://badge.fury.io/py/carnival)
[![PyPI](https://img.shields.io/pypi/pyversions/carnival.svg)](https://pypi.python.org/pypi/carnival)
[![Documentation Status](https://readthedocs.org/projects/carnival/badge/?version=latest)](https://carnival.readthedocs.io/)

![MIT](https://img.shields.io/github/license/carnival-org/carnival)

Software provisioning tool

* Runs on MacOs and Linux
* Tested on Ubuntu and CentOS
* Uses mypy strict typing mode [mypy.ini](mypy.ini)
* Safe, full run chain is validated before run

# Example
See [carnival_tasks_example.py](carnival_tasks_example.py)

## Install
```bash
$ pip3 install carnival
```

## Docs
Documentation available at [readthedocs.org](https://carnival.readthedocs.io/ru/latest/)

### Competion
* for *Bash*: place `eval "$(_CARNIVAL_COMPLETE=bash_source carnival)"` in .bashrc
* for *ZSH*: place `eval "$(_CARNIVAL_COMPLETE=zsh_source carnival)"` in .zshrc

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
