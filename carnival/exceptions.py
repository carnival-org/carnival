

class CarnivalException(BaseException):
    """
    Base error class
    """


class ContextBuilderError(CarnivalException):
    """
    Error when build context for step
    """


class ContextBuilderPassAllArgs(CarnivalException):
    """
    Signal to send full context to step with **kwargs
    """


class GlobalConnectionError(CarnivalException):
    """
    Global connection switching error
    """
