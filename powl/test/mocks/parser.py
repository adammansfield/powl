"""Provides a mock parser to set the expected output."""

class MockParser:

    def __init__(self):
        self_output = ""

    @property
    def output(self):
        """Get the output of the parse() method."""
        return self._output

    @output.setter
    def output(self, value)
        """Set the output of the parse() method."""
        self._output = value

    def parse(self, message):
        """Return the mock output."""
        return self._output

