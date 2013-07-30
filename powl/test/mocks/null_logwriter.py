"""Provides a mock null object for logging."""

class NullLogWriter(object):

    def __init__(self, folder, level=logging.INFO):
        pass

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
