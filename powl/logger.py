import logging
import os
import time

class Logger:
    """Class for logging messages to stream and to file."""

    # LOG FILE
    log_dir = 'logs'
    filename_base = time.strftime('%Y-W%W', time.localtime())
    filename_extension = 'log'
    filename = filename_base + '.' + filename_extension

    # FORMAT
    log_format = '%(asctime)s\t%(levelname)s\t%(message)s'
    log_dateformat = '%m-%d %H:%M'
    formatter = logging.Formatter(log_format, log_dateformat)

    # LOGGING
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

    # HANDLERS
    def set_file_handler(self, filedir):
        """Set file, level, and format for the log to file messages."""
        filepath = os.path.join(filedir, self.filename)
        handler = logging.FileHandler(filepath)
        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def set_stream_handler(self):
        """Set level and format for the stream messages."""
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(self.level)
        streamhandler.setFormatter(self.formatter)
        self.logger.addHandler(streamhandler)

    # INITIALIZATION
    def __init__(self, name='', output_dir='', level=logging.DEBUG):
        """Initialize the stream and file handlers."""
        self.name = name
        self.level = level
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.set_stream_handler()
        if output_dir:
            log_dir = os.path.join(output_dir, self.log_dir)
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir)
            self.set_file_handler(log_dir)
