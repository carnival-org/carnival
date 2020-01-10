# Inventory
Inventory is group of hosts.
* `role` role for host
* `address` host address  
    * `local` or `localhost` for local shell execution 
    * ip or hostname or user@hostname for ssh execution 
* `context` - additional context for runtime use

## Lets define our inventory
One role `db`  
Host's ssh connection address `1.2.3.4`      
Context variable `contextvar`  

and another `1.2.3.5` with similar fields.

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
