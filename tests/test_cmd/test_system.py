import pytest
from carnival import cmd, global_context

KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzlL9Wo8ywEFXSvMJ8FYmxP6HHHMDTyYAWwM3AOtsc96DcYVQIJ5VsydZf5/4NWuq55MqnzdnGB2IfjQvOrW4JEn0cI5UFTvAG4PkfYZb00Hbvwho8JsSAwChvWU6IuhgiiUBofKSMMifKg+pEJ0dLjks2GUcfxeBwbNnAgxsBvY6BCXRfezIddPlqyfWfnftqnafIFvuiRFB1DeeBr24kik/550MaieQpJ848+MgIeVCjko4NPPLssJ/1jhGEHOTlGJpWKGDqQK+QBaOQZh7JB7ehTK+pwIFHbUaeAkr66iVYJuC05iA7ot9FZX8XGkxgmhlnaFHNf0l8ynosanqt example@laptop"  # noqa


@pytest.mark.remote
def test_ssh_authorized_keys_list(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                assert cmd.system.ssh_authorized_keys_list() == []
                cmd.system.ssh_authorized_keys_add(KEY)
                keys = cmd.system.ssh_authorized_keys_list()
                assert len(keys) == 1
                assert KEY in keys

                # Check not added second time
                cmd.system.ssh_authorized_keys_add(KEY)
                keys = cmd.system.ssh_authorized_keys_list()
                assert len(keys) == 1
                assert KEY in keys

                cmd.cli.run("rm ~/.ssh/authorized_keys", hide=True)


@pytest.mark.remote
def test_ssh_authorized_keys_ensure(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                assert cmd.system.ssh_authorized_keys_list() == []
                cmd.system.ssh_authorized_keys_ensure(KEY)
                keys = cmd.system.ssh_authorized_keys_list()
                assert len(keys) == 1
                assert KEY in keys

                # Check not added second time
                cmd.system.ssh_authorized_keys_ensure(KEY)
                keys = cmd.system.ssh_authorized_keys_list()
                assert len(keys) == 1
                assert KEY in keys

                cmd.cli.run("rm ~/.ssh/authorized_keys", hide=True)


@pytest.mark.remote
def test_get_current_user_name(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                assert cmd.system.get_current_user_name() == 'root'


@pytest.mark.remote
def test_get_current_user_id(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                assert cmd.system.get_current_user_id() == 0


@pytest.mark.remote
def test_is_current_user_root(suspend_capture, ubuntu_ssh_host, centos_ssh_host):
    for host in [ubuntu_ssh_host, centos_ssh_host]:
        with suspend_capture:
            with global_context.SetContext(host):
                assert cmd.system.is_current_user_root() is True
