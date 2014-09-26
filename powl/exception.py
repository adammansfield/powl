"""Provides methods for extending exceptions."""

class _Message(object):
    """
    Class for storing custom error messages in exceptions.
    """

    def __init__(self, str):
        self._str = str

    def __str__(self):
        return self._str


def add_message(exception, message):
    """
    Embeds an error message into an exception that can be retrieved by
    try_get_error_message().

    Parameters
    ----------
    exception : Exception
    message : str
    """
    exception.args += (_Message(message),)


def create(exception_type, message):
    """
    Create an exception with a formatted expression and with an embedded
    message.

    Parameters
    ----------
    exception_type : type
        Type must be or inherit Exception.
    message : str
        Message to embed and to be default exception expression.

    Returns
    -------
    exception_type
    """
    expression = "{0}: {1}".format(exception_type.__name__, message)
    err = exception_type(expression)
    add_message(err, message)
    return err


def get_message(exception):
    """
    Trys to get an error message embedded in an exception.

    Parameters
    ----------
    exception : Exception

    Returns
    -------
    str
    """
    messages = [m for m in exception.args if isinstance(m, _Message)]
    if len(messages) > 0:
        return str(messages[0])
    else:
        return ""

