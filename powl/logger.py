import logging
import os
import time

# CONSTANTS
_EXTENSION = 'log'
_MESSAGE_FORMAT = '%(asctime)s\t%(levelname)s\t%(message)s'

# DAILY FORMAT
_daily_message_dateformat = '%H:%M'
_daily_formatter = logging.Formatter(_MESSAGE_FORMAT, _daily_message_dateformat)
_daily_filebase = time.strftime('%Y-%m-%d', time.localtime())
_daily_filename = _daily_filebase + '.' + _EXTENSION

# WEEKLY FORMAT
_weekly_message_dateformat = '%m-%d %H:%M'
_weekly_formatter = logging.Formatter(_MESSAGE_FORMAT, _weekly_message_dateformat)
_weekly_filebase = time.strftime('%Y-W%W', time.localtime())
_weekly_filename = _weekly_filebase + '.' + _EXTENSION

# FORMAT TYPES
FORMAT_TYPE_DAILY = 'FORMAT_TYPE_DAILY'
FORMAT_TYPE_WEEKLY = 'FORMAT_TYPE_WEEKLY'

# DEFAULTS
_DEFAULT_FORMAT_TYPE = FORMAT_TYPE_DAILY
_DEFAULT_FILENAME = _daily_filename
_DEFAULT_FORMATTER = _daily_formatter

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
        formatter = _daily_formatter
        filename = _daily_filename
    elif format_type == FORMAT_TYPE_WEEKLY:
        formatter = _weekly_formatter
        filename = _weekly_filename
    else:
        formatter = _DEFAULT_FORMATTER
        filename = _DEFAULT_FILENAME
    _set_stream_handler(level, formatter)
    if directory:
        if not os.path.isdir(directory):
            os.makedirs(directory)
        if os.path.isdir(directory):
            _set_file_handler(directory, level, formatter)
