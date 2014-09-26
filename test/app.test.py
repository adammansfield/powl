#!/usr/bin/env python
"""Tests for powl.app."""
import injector
import unittest
from powl import log
from powl import app
from test.mock import filesystem as mock_filesystem
from test.mock import log as mock_log
from test.mock import parser as mock_parser

class TestApp(unittest.TestCase):
    """
    Class for testing powl.powl.App.
    """

    def setUp(self):
        self._injector = injector.Injector(self.configure_injector)
        self._app = App(self._injector)

    def configure_injector(self, binder):
        binder.bind(log.Log, to=mock_log.MockLog)

    def test__note__input_mail_output_file(self):
        """
        Test end to end for the note action.
        """
        note = "reminder to test note"

        # TODO add note to return value of retriever.get_action_items()
        self._app.run()

        # TODO read the mock file to get the actual output
        actual_file_output = ""
        expected_file_output = note
        self.assertEqual(expected_file_output, actual_file_output)

if __name__ == '__main__':
    unittest.main()

