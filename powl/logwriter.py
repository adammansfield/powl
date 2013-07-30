"""Provides methods for logging to file and stream."""
import logging
import time

class LogWriter(object):
    """
    Provides methods for writing log messages of various levels to file and stream handlers.
    """

    _EXTENSION = ".log"
    _MESSAGE_FORMAT = "%(asctime)s\t%(levelname)s\t%(message)s"
    _DATE_FORMAT = "%H:%M"

    def __init__(self, folder, level=logging.INFO):
        """
        Initialize logger. Create and attach logging handlers. Create log file.

        Args:
            folder (powl.filesystem.Folder): Folder where the log file will be stored.
        """
        self._logger = logging.getLogger()

        formatter = logging.Formatter(self._MESSAGE_FORMAT, self._DATE_FORMAT)
        filename = time.strftime('%Y-%m-%d', time.localtime()) + self._EXTENSION
        filestream = folder.get_file(filename)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(filestream.path)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def critical(self, message, *args, **kwargs):
        """
        Log a critical message.
        """
        self._logger.critical(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """
        Log a debug message.
        """
        self._logger.debug(message, *args, **kwargs) 

    def error(self, message, *args, **kwargs):
        """
        Log a error message.
        """
        self._logger.error(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """
        Log a info message.
        """
        self._logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """
        Log a warning message.
        """
        self._logger.warning(message, *args, **kwargs)

