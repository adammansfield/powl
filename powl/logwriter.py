"""Provides methods for logging to a file and a stream."""
import logging
import time

class LogWriter(object):
    """
    Provides methods for writing log messages of various levels to file and stream handlers.
    """

    _MESSAGE_FORMAT = "%(asctime)s\t%(levelname)s\t%(message)s"
    _MESSAGE_DATE_FORMAT = "%H:%M"
    _FILENAME_DATE_FORMAT = "%Y-%m-%d"
    _FILENAME_EXTENSION = ".log"

    def __init__(self, folder, level=logging.INFO):
        """
        Initialize logger. Create and attach logging handlers. Create log file.

        Args:
            folder (powl.filesystem.Folder): Folder where the log file will be stored.
            level (int): Optional log level of the handlers.
        """
        self._logger = logging.getLogger()

        formatter = logging.Formatter(self._MESSAGE_FORMAT, self._MESSAGE_DATE_FORMAT)
        filename = time.strftime(self._FILENAME_DATE_FORMAT, time.localtime()) + self._FILENAME_EXTENSION
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

        Args:
            message (string): Message to log.
            args (strings, ints, or floats): Arguments to be merged into message.
            kwargs (dict): Arguments used for user defined attributes.
        """
        self._logger.critical(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """
        Log a debug message.

        Args:
            message (string): Message to log.
            args (strings, ints, or floats): Arguments to be merged into message.
            kwargs (dict): Arguments used for user defined attributes.
        """
        self._logger.debug(message, *args, **kwargs) 

    def error(self, message, *args, **kwargs):
        """
        Log an error message.

        Args:
            message (string): Message to log.
            args (strings, ints, or floats): Arguments to be merged into message.
            kwargs (dict): Arguments used for user defined attributes.
        """
        self._logger.error(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """
        Log an info message.

        Args:
            message (string): Message to log.
            args (strings, ints, or floats): Arguments to be merged into message.
            kwargs (dict): Arguments used for user defined attributes.
        """
        self._logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """
        Log a warning message.

        Args:
            message (string): Message to log.
            args (strings, ints, or floats): Arguments to be merged into message.
            kwargs (dict): Arguments used for user defined attributes.
        """
        self._logger.warning(message, *args, **kwargs)
