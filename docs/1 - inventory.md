# Lets define our inventory

Host's ssh connection address `1.2.3.4`  
One role `db`  
Context variable `contextvar`

and another similar

```python
from carnival import inv, task
from carnival import context

inv.host(role='db', '1.2.3.4', contextvar="Hello")
inv.host(role='db', '1.2.3.5', contextvar="World")
```

## Host context
Host context available in task at `carnival.context.host_context`

```python
@task()
def our_task():
    print(context['contextvar'])
```


Run on our hosts outputs:  
```bash
Hello
World
```
