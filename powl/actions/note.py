"""Action to process a note."""
from powl.actions.fileaction import FileAction

class Note(FileAction):

    # PROCESSING
    def process(self):
        """Process the data into the proper output format."""
        self._output_data = self._input_data
