"""Provides mock objects for powl.log."""

class MockLog(object):
    """
    Provides a mock null object for powl.log.Log.
    """

    def critical(self, message, *args, **kwargs):
        pass

    def debug(self, message, *args, **kwargs):
        pass

    def error(self, message, *args, **kwargs):
        pass

    def info(self, message, *args, **kwargs):
        pass

    def warning(self, message, *args, **kwargs):
        pass

