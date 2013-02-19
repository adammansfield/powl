"""Superclass to perform actions with input data."""

class Action:
    
    # PROCESSING
    def input(self, data, date):
        """Set the data and date to be used."""
        self._input_data = data
        self._input_date = date

    def process(self):
        """Process the data into the proper output format."""
        pass

    def output(self):
        """Output the processed data through the specified means."""
        pass

    # INITIALIZATION
    def initialize(self):
        """Initialize any resources needed for output."""
        pass

    def __init__(self):
        """Set the initial values."""
        self._input_data = None
        self._input_date = None
        self._output_data = None
