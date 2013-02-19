"""Superclass for actions to output to a file."""
import powl.output as output
from powl.actions.action import Action

class FileAction(Action):

    # PROCESSING
    def output(self):
        """Output the processed data through the specified means."""
        if not self._output_filepath:
            output.append(self._output_filepath, self._output_data)

    # INITIALIZATION
    def initialize(self):
        """Create output directories."""
        if not self.__directories:
            output.makedir(self.__directories)

    def __init__(self):
        """Set the initial values."""
        super(FileAction, self).__init__()
        self.__directories = None
        self._output_filepath = None

    def __init__(self, directories):
        """Set the initial values and output directories."""
        super(FileAction, self).__init__()
        self.__directories = directories
        self._output_filepath = None
