import logging
import os
import time

logger = logging.getLogger()
level = logging.DEBUG
logger.setLevel(level)
format = '%(asctime)s\t%(levelname)s\t%(message)s'
dateformat = '%H:%M'
formatter = logging.Formatter(format, dateformat)

filedir = os.getcwd() + os.sep + 'logs'
filename = time.strftime('%Y-%m-%d', time.localtime()) + '.log'
file = filedir + os.sep + filename
filehandler = logging.FileHandler(file)
filehandler.setLevel(level)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

streamhandler = logging.StreamHandler()
streamhandler.setLevel(level)
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)

def critical(message, *args, **kwargs):
    """Uses the predefined logger to log a critical message."""
    logger.critical(message, *args, **kwargs)

def debug(message, *args, **kwargs):
    """Uses the predefined logger to log a debug message."""
    logger.debug(message, *args, **kwargs) 

def error(message, *args, **kwargs):
    """Uses the predefined logger to log a error message."""
    logger.error(message, *args, **kwargs)

def info(message, *args, **kwargs):
    """Uses the predefined logger to log a info message."""
    logger.info(message, *args, **kwargs)

def warning(message, *args, **kwargs):
    """Uses the predefined logger to log a warning message."""
    logger.warning(message, *args, **kwargs)
