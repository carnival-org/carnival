import pytest

from carnival import secrets_manager
from carnival.secrets_manager import SecretGetter


def test_secrets_manager():
    with pytest.raises(NotImplementedError):
        SecretGetter().get_secret("TEST")


def test_secrets_manager_static():
    assert secrets_manager.secrets_storage == {}

    secrets_manager.secret("STATIC_SECRET", secrets_manager.Static("SECRET_VALUE"))
    assert secrets_manager.secrets_storage['STATIC_SECRET'] == 'SECRET_VALUE'

    secrets_manager.secrets_storage = {}


def test_secrets_manager_from_cli(mocker):
    assert secrets_manager.secrets_storage == {}

    mocker.patch('getpass.getpass', new=lambda p: "SECRET_VALUE")
    secrets_manager.secret("STATIC_SECRET", secrets_manager.FromCli())
    assert secrets_manager.secrets_storage['STATIC_SECRET'] == 'SECRET_VALUE'
    secrets_manager.secrets_storage = {}


def test_secrets_manager_from_env(mocker):
    assert secrets_manager.secrets_storage == {}
    mocker.patch('os.getenv', new=lambda v, d: None)
    secrets_manager.secret("STATIC_SECRET", secrets_manager.FromEnv(default="123", required=False))
    assert secrets_manager.secrets_storage['STATIC_SECRET'] == '123'
    secrets_manager.secrets_storage = {}

    with pytest.raises(secrets_manager.SecretGetError):
        assert secrets_manager.secrets_storage == {}
        mocker.patch('os.getenv', new=lambda v, d: None)
        secrets_manager.secret("STATIC_SECRET", secrets_manager.FromEnv(default="123", required=True))
        secrets_manager.secrets_storage = {}

    assert secrets_manager.secrets_storage == {}
    mocker.patch('os.getenv', new=lambda v, d: "SECRET_VALUE")
    secrets_manager.secret("STATIC_SECRET", secrets_manager.FromEnv(required=True))
    assert secrets_manager.secrets_storage['STATIC_SECRET'] == 'SECRET_VALUE'
    secrets_manager.secrets_storage = {}
