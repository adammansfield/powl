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

    def set_file_handler(self, filedir):
        """Set file to which to direct log messages."""
        filename = time.strftime('%Y-%m-%d', time.localtime()) + '.log'
        file = filedir + os.sep + filename
        handler = logging.FileHandler(file)
        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def set_stream_handler(self):
        """Set level and format for the stream messages."""
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(self.level)
        streamhandler.setFormatter(self.formatter)
        self.logger.addHandler(streamhandler)

    def __init__(self, loggername="", filedir="", level=logging.DEBUG):
        """Initialize the file and stream handlers."""
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(level)
        logformat = '%(asctime)s\t%(levelname)s\t%(message)s'
        dateformat = '%H:%M'
        self.formatter = logging.Formatter(logformat, dateformat)
        self.level = level
        self.set_stream_handler()
        if filedir != "":
            self.set_file_handler(filedir)
