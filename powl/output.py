#!/usr/bin/env python
"""Safely output to the filesystem."""
import errno
import os

def append(filepath, data):
    """Safely append data to the specified file."""
    try:
        with open(filepath, 'a') as fp:
            fp.write(data)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def write(filepath, data):
    """Safely write data (with backup if exists) to the specified file."""
    if not os.path.isfile(filepath):
        _write(filepath, data)
    else:
        backupfile = filepath + '.bak'
        tempfile = filepath + '.tmp'
        os.rename(filepath, backupfile)
        _write(tempfile, data)
        if os.path.isfile(tempfile):
           os.rename(tempfile, filepath) 
           os.remove(backupfile)

def _write(filepath, data):
    """Safely write data to the specified file."""
    try:
        with open(filepath, 'w') as fp:
            fp.write(data)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def makedir(directories):
    """Safely and recursively make the specified directories."""
    for directory in directories:
        if not os.path.isdir(directory):
            _makedir(directory)

def _makedir(directory):
    """Safely make the specified directory."""
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
