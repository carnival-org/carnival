# Task
Task is entrypoint, that can runs step or other tasks.


## Example
```python
from carnival import Step, cmd, Task, Host, SimpleTask

host = Host("1.2.3.4", packages=["htop", ])


class Frontend(Step):
    def run(self, **kwargs):
        cmd.apt.install_multiple("htop")
        cmd.docker.install_ce_ubuntu()
        cmd.docker.install_compose()

class OtherTask(Task):
    def run(self, **kwargs):
        pass

class SetupFrontend(Task):
    def run(self, **kwargs):
        self.step(Frontend(), host)  # call step on host
        self.call_task(OtherTask)  # call another task
```


### SimpleTask
Shortcut class for simple run all `steps` on all `hosts`
```python
class SetupOther(SimpleTask):
    steps = [Frontend, ]
    hosts = [host, ]
```

Run this tasks
```bash
$ carnival other_task
$ carnival setup_frontend
$ carnival setup_other
```


## Task naming
Task named from two parts. Task class name and relative task module path.  
Tasks, written in `carnival_tasks` and [internal tasks](../carnival/internal_tasks.py) module has no module part.
For example:
```
<carnival root>/
  carnival_tasks.py
  servers/__init__.py
  servers/nginx.py <- class Restart(Task): ...
```
`Restart(Task)` full name will be `servers.nginx.restart`.
```bash
$ carnival servers.nginx.restart #  Calls servers.nginx.Restart(Task)
```  

You can change this, just set `Task.name` for name, `Task.module_name` for module part.    
`Task.name` cannot be empty string.  
If `Task.module_name` is empty string - task has no module part.  
