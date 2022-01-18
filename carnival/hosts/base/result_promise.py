import io
from threading import Thread
import sys
import typing
import abc

from colorama import Fore as F  # type: ignore

from .result import Result


class ResultPromise:
    command: str
    stdout: typing.IO[bytes]
    stderr: typing.IO[bytes]

    @abc.abstractmethod
    def is_done(self) -> bool: ...

    @abc.abstractmethod
    def wait(self) -> int: ...

    def get_result(self, hide: bool, show_command: bool = False) -> Result:
        """
        Получить результат

        :param hide: скрыть stderr & stdout
        :param show_command: показать исполняемую команду
        """
        if show_command is True:
            print(f"{F.GREEN}${F.RESET} {self.command}")

        if hide is True:
            retcode = self.wait()
            return Result(
                return_code=retcode,
                stderr=self.stderr.read().decode(),
                stdout=self.stdout.read().decode(),
                command=self.command,
            )

        # Копируем stdout & stderr команды на экран и в буферы
        # чтобы вернуть результат
        threads = []

        cmd_stdout = io.BytesIO()
        cmd_stderr = io.BytesIO()

        def output_thread(fromio: typing.IO[bytes], toios: typing.List[typing.IO[bytes]]) -> None:
            while not self.is_done():
                try:
                    data = fromio.read(1)
                except IOError:
                    continue
                for toio in toios:
                    toio.write(data)
                    toio.flush()

            data = fromio.read()
            for toio in toios:
                toio.write(data)
                toio.flush()

        threads.append(Thread(target=output_thread, args=(self.stdout, [sys.stdout.buffer, cmd_stdout])))
        threads.append(Thread(target=output_thread, args=(self.stderr, [sys.stderr.buffer, cmd_stderr])))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        cmd_stdout.seek(0)
        cmd_stderr.seek(0)

        retcode = self.wait()
        return Result(
            return_code=retcode,
            stderr=cmd_stderr.read().decode(),
            stdout=cmd_stdout.read().decode(),
            command=self.command,
        )
