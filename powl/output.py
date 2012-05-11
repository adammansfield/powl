#!/usr/bin/env python
"""Manage the output of powl to the filesystem."""
import errno
import os

class Output:
    """Manage the output of powl to the filesystem."""

    def append(filepath, data):
        """Append data to the specified file."""
        if os.path.isfile(filepath):
            with open(filepath, 'a') as fp:
                fp.write(data)

    def write(filepath, data):
        """Write data to the specified file."""
        if os.path.isfile(filepath):
            with open(filepath, 'w') as fp:
                fp.write(data)

    def makedir(directories):
        """Make the specified directories."""
        for directory in directories:
            if not os.path.isdir(directory):
                try:
                    os.makedirs(directory)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
