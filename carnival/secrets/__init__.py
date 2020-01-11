import warnings
import getpass
import os

from carnival import global_context
from carnival.secrets.base import SecretGetter


def secret(var_name: str, secret_get_method: SecretGetter):
    if var_name in global_context.secrets.keys():
        warnings.warn(f"Secret {var_name} already defined. Skipping.")

    global_context.secrets[var_name] = secret_get_method.get_secret(var_name)


class Static(SecretGetter):
    def __init__(self, value: str):
        self._value = value

    def get_secret(self, var_name: str):
        return self._value


class FromCli(SecretGetter):
    """
    Ask in cli
    """
    def get_secret(self, var_name: str):
        return getpass.getpass(f"{var_name}> ")


class FromEnv(SecretGetter):
    """
    Get from environment
    """
    def __init__(self, default=None, required=False):
        self.default = default
        self.required = required

    def get_secret(self, var_name: str):
        res = os.getenv(var_name, None)
        if res is None:
            if self.required is True:
                raise ValueError(f"{var_name} is not set in environment")
            return self.default
        return res
