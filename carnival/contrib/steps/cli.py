import typing

from carnival import Step, Connection


class OpenShell(Step):
    """
    Запустить интерактивный шелл в папке
    """

    def __init__(self, shell_cmd: str = "/bin/bash", cwd: typing.Optional[str] = None) -> None:
        """
        :param shell_cmd: команда для запуска шелла
        :param cwd: папка
        """
        self.shell_cmd = shell_cmd
        self.cwd = cwd

    def run(self, c: "Connection") -> typing.Any:
        c.run(self.shell_cmd, cwd=self.cwd)
