"""Provides mock objects for powl.action."""

class MockAction(object):
    """
    Provides a mock object for powl.action.Action.
    """

    def __init__(self):
        self._do_called = False
        self._do_string = ""
        self._do_date = ""

    def do_called_with(self, string, date):
        return (self._do_called and
                self._do_string == string and
                self._do_date == date)

    # powl.action.Action methods.
    def do(self, string, date):
        self._do_called = True
        self._do_string = string
        self._do_date = date

