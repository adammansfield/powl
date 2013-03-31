"""Superclass to perform actions with input data."""

class Action(object):
    
    # I/O
    def input(self, data, date):
        """Parse the input data and date into usable parameters."""
        raise NotImplementedError("Subclass must implement abstract method.")

    def output(self):
        """Output the processed data through the specified means."""
        raise NotImplementedError("Subclass must implement abstract method.")

    # PROCESSING
    def process(self):
        """Process the data into the proper output format."""
        raise NotImplementedError("Subclass must implement abstract method.")

    # INITIALIZATION
    def initialize(self):
        """Initialize any resources needed for output."""
        raise NotImplementedError("Subclass must implement abstract method.")

    def __init__(self):
        """Set the initial values."""
        raise NotImplementedError("Subclass must implement abstract method.")
