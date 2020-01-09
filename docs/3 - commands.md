# Commands
`
$ grep -r def carnival/cmd | sed -e 's/.py:def /./g' | sed -e 's/\//./g' | sed -e 's/carnival.//g'
`

```
cmd.system.set_password(username: str, password: str):

cmd.systemd.start(service_name: str, daemon_reload=False):
cmd.systemd.stop(service_name: str, daemon_reload=False):
cmd.systemd.enable(service_name: str, daemon_reload=False, start_now=True):
cmd.systemd.disable(service_name: str, daemon_reload=False, stop_now=True):

cmd.docker.install_ce(version=None) -> bool:
cmd.docker.install_compose(version="1.25.1", dest=".usr.local.bin.docker-compose"):

cmd.cli.run(command: str, **kwargs):

cmd.apt.get_installed_version(pkgname: str) -> Optional[str]:
cmd.apt.is_pkg_installed(pkgname: str, version=None) -> bool:
cmd.apt.force_install(pkgname, version=None, update=False):
cmd.apt.install(pkgname, version=None, update=True) -> bool:
cmd.apt.install_multiple(*pkg_names: str, update=True):
```

## Lets enable nginx
```python
from carnival import cmd, task

@task()
def t():
    cmd.systemd.enable("nginx")
```
