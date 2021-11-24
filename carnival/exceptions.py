

class CarnivalException(BaseException):
    """
    Base error class
    """


class GlobalConnectionError(CarnivalException):
    """
    Global connection switching error
    """


class StepValidationError(CarnivalException):
    """
    Ошибка валидации шага
    """
