"""Provides mock objects for powl.action."""

class MockAction(object):
    """
    Provides a mock object for powl.action.Action.
    """

    def __init__(self):
        self._do_called = False

    @property
    def do_called(self):
        return self._do_called

    # powl.action.Action methods.
    def do(self, string, date):
        self._do_called = True

