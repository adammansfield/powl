#!/usr/bin/env python
"""Module for easily directing logging output to streams and files."""
import errno
import logging
import os
import time

class LogWriter(object):

    def __init__(self, formatter, path, filename, level=logging.INFO):
        """Get a logger and set stream and file handlers."""
        self._logger = logging.getLogger()
        self._logger.setLevel(level) 
        self._set_stream_handler(formatter, level)
        self._set_file_handler(formatter, level, path, filename)

    def critical(self, message, *args, **kwargs):
        """Log a critical message."""
        self._logger.critical(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """Log a debug message."""
        self._logger.debug(message, *args, **kwargs) 

    def error(self, message, *args, **kwargs):
        """Log a error message."""
        self._logger.error(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """Log a info message."""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Log a warning message."""
        self._logger.warning(message, *args, **kwargs)

    def _set_stream_handler(self, formatter, level):
        """Set level and format for the trace messages."""
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def _set_file_handler(self, formatter, level, path, filename):
        """Set file path, level, and format for log messages."""
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        filepath = os.path.join(path, filename)
        handler = logging.FileHandler(filepath)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

