from carnival import inv, cmd, task

inv.host('frontend', '1.2.3.4', localip="127.0.0.1")
inv.host('frontend', '1.2.3.4', localip="127.0.0.1")

inv.host('backend', '1.2.3.4', localip="127.0.0.1")
inv.host('database', '1.2.3.4', localip="127.0.0.1")


@task(roles=['frontend'])
def initialize_host(**host_context):
    cmd.apt.install_multiple('htop', 'httpie')
    cmd.docker.install_ce()
    cmd.docker.install_compose()
