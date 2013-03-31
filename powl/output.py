#!/usr/bin/env python
"""Safe output to the filesystem."""
import errno
import os

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

