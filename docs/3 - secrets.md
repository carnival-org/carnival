# Secrets management utils.
Secrets are data, stored somewhere out of codebase, 
and need to be set runtime.  
Then you can access secrets in role `run` method with `global_context` property


## Secret getters
* secrets.FromCli() - from cli
* secrets.FromEnv(self, default=None, required=False) - from env

# Example
```python
from carnival import secrets, Role, Host, global_context

# Tell how to get secret
secrets.secret("root_password", secrets.FromCli())

class Frontend(Role):
    hosts = [
        Host("1.2.3.4"),
    ]

    def run(self):
        print(global_context.secrets['root_password'])
```
