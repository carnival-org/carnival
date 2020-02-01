# Commands
`
$ grep -r def carnival/cmd | sed -e 's/.py:def /./g' | sed -e 's/\//./g' | sed -e 's/carnival.//g'
`

```
cmd.system.set_password(username: str, password: str):
cmd.system.ssh_append_id(ssh_key: str, keys_file=".ssh.authorized_keys"):
cmd.system.ssh_ensure_keys(ssh_keys: List[str]):

cmd.systemd.daemon_reload():
cmd.systemd.start(service_name: str, reload_daemon=False):
cmd.systemd.stop(service_name: str, reload_daemon=False):
cmd.systemd.restart(service_name: str):
cmd.systemd.enable(service_name: str, reload_daemon=False, start_now=True):
cmd.systemd.disable(service_name: str, reload_daemon=False, stop_now=True):

cmd.docker.install_ce(version=None) -> bool:
cmd.docker.install_compose(version="1.25.1", dest=".usr.local.bin.docker-compose"):

cmd.transfer.rsync(source, target, exclude=(), delete=False, strict_host_keys=True, rsync_opts="--progress -pthrvz", ssh_opts=''):
cmd.transfer.get(remote: str, local: str, preserve_mode: bool = True) -> Result:
cmd.transfer.put(local: str, remote: str, preserve_mode: bool = True) -> Result:
cmd.transfer.put_template(template_path: str, remote: str, **context) -> Result:
cmd.transfer.is_file_contains(filename, text, exact=False, escape=True):
cmd.transfer.is_file_exists(path) -> bool:
cmd.transfer.is_dir_exists(path, user=None, group=None, mode=None) -> bool:

cmd.cli._run_command(command: str, **kwargs):
cmd.cli.run(command: str, **kwargs):
cmd.cli.pty(command: str, **kwargs):
cmd.cli.mkdirs(*dirs: str):

cmd.apt.get_installed_version(pkgname: str) -> Optional[str]:
cmd.apt.is_pkg_installed(pkgname: str, version=None) -> bool:
cmd.apt.force_install(pkgname, version=None, update=False):
cmd.apt.install(pkgname, version=None, update=True) -> bool:
cmd.apt.install_multiple(*pkg_names: str, update=True):
```

## Lets enable nginx
```python
from carnival import Step, cmd

class Frontend(Step):
    def run(self, to_enable):
        cmd.systemd.enable(to_enable)
```
