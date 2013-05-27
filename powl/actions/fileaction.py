"""Superclass for actions to output to a file."""
import errno
import os
from powl.actions.action import Action

class FileAction(Action):

    # I/O
    def output(self):
        """Output the processed data to the specified file."""
        if self._output_filepath:
            self._append_file(self._output_filepath,
                              self._output_data)

    def _append_file(filepath, data):
        """Safely append data to the specified file."""
        try:
            with open(filepath, 'a') as fp:
                fp.write(data)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def _makedir(self, directory):
        """Safely make the specified directory."""
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # INITIALIZATION
    def init(self, directories):
        """Create output directories."""
        for directory in directories:
            if not os.path.isdir(directory):
                self._makedir(directory)

    def __init__(self, output_filepath=""):
        """Initiliaze members."""
        self._output_filepath = output_filepath
        self._output_data = ""
