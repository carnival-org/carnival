# Secrets management utils.
Secrets are data, stored somewhere out of codebase, 
and need to be set runtime.  
Then you can access secrets, adding `secrets` arg in Step's `run` method


## Secret getters
* secrets.Static(value: str) - static hardcoded secret for testing
* secrets.FromCli() - from cli
* secrets.FromEnv(self, default=None, required=False) - from env

# Example
```python
from carnival import secrets_manager, Step

# Tell how to get secret
secrets_manager.secret("root_password", secrets_manager.FromCli())

class Frontend(Step):
    def run(self, secrets):
        print(secrets['root_password'])
```
