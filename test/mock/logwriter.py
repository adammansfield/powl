"""Provides a mock null object for logging."""

class MockLogWriter(object):

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

