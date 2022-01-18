
class CommandError(BaseException):
    pass


class Result:
    """
    Результат выполнения команды
    """

    def __init__(
            self,
            return_code: int,
            stderr: str,
            stdout: str,
            command: str,
    ) -> None:
        """
        :param return_code: код возврата
        :param stderr: содержимое stderr
        :param stdout: содержимое stdout
        :param command: команда, которая была запущена

        """
        self.command = command
        self.return_code = return_code
        self.stderr = stderr.replace("\r", "").strip()
        self.stdout = stdout.replace("\r", "").strip()

    def check_result(self, warn: bool, hide: bool) -> None:
        """
        Проверить результат выполнения, выкинуть ошибку если она была

        :param warn: вывести результат неуспешной команды вместо того чтобы выкинуть исключение :py:exc:`.CommandError`
        """
        if not self.ok:
            if warn:
                if not hide:
                    if self.stdout:
                        print(self.stdout, flush=True)
                    if self.stderr:
                        print(self.stderr, flush=True)

            if not warn:
                if self.stdout:
                    print(self.stdout, flush=True)
                if self.stderr:
                    print(self.stderr, flush=True)
                raise CommandError(f"{self.command} failed with exist code: {self.return_code}")

    @property
    def ok(self) -> bool:
        return self.return_code == 0
