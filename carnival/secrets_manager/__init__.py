import warnings
import getpass
import os
from typing import Dict, Any

from carnival.secrets_manager.base import SecretGetter


secrets_storage: Dict[str, Any] = {}


def secret(var_name: str, secret_get_method: SecretGetter):
    if var_name in secrets_storage.keys():
        warnings.warn(f"Secret {var_name} already defined. Skipping.")

    secrets_storage[var_name] = secret_get_method.get_secret(var_name)


class SecretGetError(Exception):
    pass


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
                raise SecretGetError(f"{var_name} is not set in environment")
            return self.default
        return res
