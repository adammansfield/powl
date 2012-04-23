import logging
import os
import time

class Logger:
    """Class for logging messages to stream and to file."""

    def critical(self, message, *args, **kwargs):
        """Uses the predefined logger to log a critical message."""
        self.logger.critical(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """Uses the predefined logger to log a debug message."""
        self.logger.debug(message, *args, **kwargs) 

    def error(self, message, *args, **kwargs):
        """Uses the predefined logger to log a error message."""
        self.logger.error(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """Uses the predefined logger to log a info message."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Uses the predefined logger to log a warning message."""
        self.logger.warning(message, *args, **kwargs)

    def __init__(self, level, filedir):
        """Initialize the file and stream handlers."""
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        format = '%(asctime)s\t%(levelname)s\t%(message)s'
        dateformat = '%H:%M'
        formatter = logging.Formatter(format, dateformat)
        filename = time.strftime('%Y-%m-%d', time.localtime()) + '.log'
        file = filedir + os.sep + filename
        filehandler = logging.FileHandler(file)
        filehandler.setLevel(level)
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(level)
        streamhandler.setFormatter(formatter)
        self.logger.addHandler(streamhandler)
