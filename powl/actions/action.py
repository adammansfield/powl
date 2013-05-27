"""Superclass to perform actions with input data."""

class Action(object):
    
    # I/O
    def input(self, data, date):
        """Set the input members."""
        self._input_data = data
        self._input_date = date

    def output(self):
        """Output the processed data through the specified means."""
        pass

    # PROCESSING
    def process(self):
        """Process the data into the proper output format."""
        pass

    # INITIALIZATION
    def init(self):
        """Initialize any resources needed for output."""
        pass

    def __init__(self):
        """Set the initial values."""
        pass
