from carnival.host import AnyConnection, Result


def run(c: AnyConnection, command: str, hide: bool = False) -> Result:
    """
    Запустить комманду и дождаться окончания

    :param command: команда для выполнения
    :param hide: скрыть результаты выполнения команды
    """
    result = c.run(command, hide=hide).wait()
    return result
