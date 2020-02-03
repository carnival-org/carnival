from carnival import cmd
from carnival.utils import log


def install_ce_ubuntu(version=None) -> bool:
    """
    Returns true if installed, false if was already installed
    """
    # https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/
    from carnival.cmd import apt
    pkgname = "docker-ce"
    if apt.is_pkg_installed(pkgname, version):
        log(f"{pkgname} already installed")
        return False

    log(f"Installing {pkgname}...")

    cmd.cli.run("sudo apt-get remove docker docker-engine docker.io")
    cmd.cli.run("sudo apt-get update")
    cmd.cli.run("sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common")
    cmd.cli.run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -", pty=True)
    cmd.cli.run('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')

    apt.force_install(pkgname=pkgname, version=version, update=True, hide=True)
    return True


def install_compose(version="1.25.1", dest="/usr/local/bin/docker-compose"):
    log(f"Installing compose...")
    download_link = f"https://github.com/docker/compose/releases/download/{version}/docker-compose-`uname -s`-`uname -m`"
    cmd.cli.run(f"sudo curl -sL {download_link} -o {dest}")
    cmd.cli.run(f"sudo chmod a+x {dest}")
