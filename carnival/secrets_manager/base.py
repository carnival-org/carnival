import abc


class SecretGetter(abc.ABC):
    def get_secret(self, var_name: str):
        raise NotImplementedError
