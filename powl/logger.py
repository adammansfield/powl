import logging
import os
import time

# CONSTANTS
_EXTENSION = 'log'
_MESSAGE_FORMAT = '%(asctime)s\t%(levelname)s\t%(message)s'

# DAILY FORMAT
_DAILY_MESSAGE_DATEFORMAT = '%H:%M'
_DAILY_FORMATTER = logging.Formatter(_MESSAGE_FORMAT, _DAILY_MESSAGE_DATEFORMAT)
_DAILY_FILEBASE = time.strftime('%Y-%m-%d', time.localtime())
_DAILY_FILENAME = _DAILY_FILEBASE + '.' + _EXTENSION

# WEEKLY FORMAT
_WEEKLY_MESSAGE_DATEFORMAT = '%m-%d %H:%M'
_WEEKLY_FORMATTER = logging.Formatter(_MESSAGE_FORMAT, _WEEKLY_MESSAGE_DATEFORMAT)
_WEEKLY_FILEBASE = time.strftime('%Y-W%W', time.localtime())
_WEEKLY_FILENAME = _WEEKLY_FILEBASE + '.' + _EXTENSION

# FORMAT TYPES
FORMAT_TYPE_DAILY = 'FORMAT_TYPE_DAILY'
FORMAT_TYPE_WEEKLY = 'FORMAT_TYPE_WEEKLY'

# DEFAULTS
_DEFAULT_FORMAT_TYPE = FORMAT_TYPE_DAILY
_DEFAULT_FILENAME = _DAILY_FILENAME
_DEFAULT_FORMATTER = _DAILY_FORMATTER

# LOGGER
_logger = None


# LOGGING
def critical(message, *args, **kwargs):
    """Uses a logger to log a critical message."""
    global _logger
    if not _logger:
        initialize()
    _logger.critical(message, *args, **kwargs)

def debug(message, *args, **kwargs):
    """Uses a logger to log a debug message."""
    global _logger
    if not _logger:
        initialize()
    _logger.debug(message, *args, **kwargs) 

def error(message, *args, **kwargs):
    """Uses a logger to log a error message."""
    global _logger
    if not _logger:
        initialize()
    _logger.error(message, *args, **kwargs)

def info(message, *args, **kwargs):
    """Uses a logger to log a info message."""
    global _logger
    if not _logger:
        initialize()
    _logger.info(message, *args, **kwargs)

def warning(message, *args, **kwargs):
    """Uses a logger to log a warning message."""
    global _logger
    if not _logger:
        initialize()
    _logger.warning(message, *args, **kwargs)

# HANDLERS
def _set_file_handler(filepath, level, formatter):
    """Set file, level, and format for the log to file messages."""
    global _logger
    handler = logging.FileHandler(filepath)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

def _set_stream_handler(level, formatter):
    """Set level and format for the stream messages."""
    global _logger
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

# INITIALIZATION
def initialize(format_type=_DEFAULT_FORMAT_TYPE, directory='', level=logging.DEBUG):
    """Get a logger and set stream and file handlers."""
    global _logger
    _logger = logging.getLogger()
    _logger.setLevel(level) 
    if format_type == FORMAT_TYPE_DAILY:
        formatter = _DAILY_FORMATTER
        filename = _DAILY_FILENAME
    elif format_type == FORMAT_TYPE_WEEKLY:
        formatter = _WEEKLY_FORMATTER
        filename = _WEEKLY_FILENAME
    else:
        formatter = _DEFAULT_FORMATTER
        filename = _DEFAULT_FILENAME
    _set_stream_handler(level, formatter)
    if directory:
        if not os.path.isdir(directory):
            os.makedirs(directory)
        if os.path.isdir(directory):
            filepath = os.path.join(directory, filename)
            _set_file_handler(filepath, level, formatter)
