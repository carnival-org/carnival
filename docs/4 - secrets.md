# Secrets management utils.
Secrets are data, stored somewhere out of codebase, 
and need to be set runtime.


## Secret getters
* secrets.FromCli() - from cli
* secrets.FromEnv(self, default=None, required=False) - from env

# Example
```python
from carnival import inv, cmd, task, secrets
from carnival import context

# Tell how to get secret
secrets.secret("ROOT_PASSWORD", secrets.FromCli())

# Define inventory
inv.host('frontend', 'root@1.2.3.4')


@task(roles=['frontend', ])
def change_frontend_password():
    # Get root password from cli and set on frontend servers
    cmd.system.set_password("frontend", context.secrets['ROOT_PASSWORD'])
