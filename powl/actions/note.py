"""Action to process a note."""
from powl.actions.fileaction import FileAction

class Note(FileAction):

    # I/O
    def input(self, data, date):
        """Parse the input data."""
        self._note = data

    # PROCESSING
    def process(self):
        """Process the data into the proper output format."""
        self._output_data = self._note

    # INITIALIZATION
    def __init__(self, filepath):
        self._output_filepath = filepath
      
