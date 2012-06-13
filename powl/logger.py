#!/usr/bin/env python
"""Module for easily directing logging output to streams and files."""
import errno
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
FORMAT_DAILY = 'FORMAT_DAILY'
FORMAT_WEEKLY = 'FORMAT_WEEKLY'

# DEFAULTS
_DEFAULT_DIR = 'logs'
_DEFAULT_FORMAT = FORMAT_DAILY
_DEFAULT_FILENAME = _DAILY_FILENAME
_DEFAULT_FORMATTER = _DAILY_FORMATTER
_DEFAULT_LEVEL = logging.DEBUG

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
def set_stream_handler():
    """Set level and format for the stream messages."""
    global _logger, _level, _formatter
    handler = logging.StreamHandler()
    handler.setLevel(_level)
    handler.setFormatter(_formatter)
    _logger.addHandler(handler)

def set_file_handler(directory):
    """Set file, level, and format for the log to file messages."""
    global _logger, _filename, _level, _formatter
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    filepath = os.path.join(directory, _filename)
    handler = logging.FileHandler(filepath)
    handler.setLevel(_level)
    handler.setFormatter(_formatter)
    _logger.addHandler(handler)

# INITIALIZATION
def initialize(format_type=_DEFAULT_FORMAT, level=_DEFAULT_LEVEL):
    """Get a logger and set stream and file handlers."""
    global _logger, _filename, _formatter, _level
    _level = level
    _logger = logging.getLogger()
    _logger.setLevel(_level) 
    if format_type == FORMAT_DAILY:
        _formatter = _DAILY_FORMATTER
        _filename = _DAILY_FILENAME
    elif format_type == FORMAT_WEEKLY:
        _formatter = _WEEKLY_FORMATTER
        _filename = _WEEKLY_FILENAME
    else:
        _formatter = _DEFAULT_FORMATTER
        _filename = _DEFAULT_FILENAME
    set_stream_handler()
