"""Provides a mock parser to set the expected output."""

class MockParser(object):

    def __init__(self):
        self._parse_string = ""
        self._parse_retval = ""

    @property
    def parse_string(self):
        return self._parse_string

    @parse_string.setter
    def parse_string(self, value)
        self._parse_string = value

    @property
    def parse_retval(self):
        return self._parse_retval

    @parse_retval.setter
    def parse_retval(self, value)
        self._parse_retval = value

    # powl.parser.Parser methods
    def parse(self, string):
        self._parse_string = string
        return self._parse_retval

