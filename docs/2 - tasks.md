# Tasks
Task is function without arguments, marked `task` decorator.
Tasks runing for work in inventory host 
connections using [commands](3%20-%20commands.md).


```python
from carnival import task

# Task for 'db' and 'backups', with set name and help
@task(roles=['db', 'backups'], task_name="test_task", help_text="Hi")
def our_task():
    pass


# Task for all roles without help text
@task(task_name="test_task2")
def our_task1():
    pass

# Task for all roles with auto-generated name (our_task2)
@task(help_text="Hi")
def our_task2():
    pass
```
