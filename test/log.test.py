#!/usr/bin/env python
"""Tests for powl.log."""
import unittest
from powl import log

class TestErrorMessageFunctions(unittest.TestCase):
    """
    Class for testing get_error_message().
    """

    def test_sanity_with_error_message(self):
        """
        Test that added message by error message can be retrieved.
        """
        error_message = log.ErrorMessage("error message")
        exception = Exception()
        log.add_error_message(exception, error_message)
        actual = log.try_get_error_message(exception)
        self.assertEqual(str(error_message), actual)

    def test_sanity_with_string(self):
        """
        Test that added message by string can be retrieved.
        """
        error_message = "error message"
        exception = Exception()
        log.add_error_message(exception, error_message)
        actual = log.try_get_error_message(exception)
        self.assertEqual(error_message, actual)

    def test__get__does_not_throw_if_no_error_message(self):
        """
        Test to ensure that empty ErrorMessage is returned if none found.
        """
        exception = Exception()
        actual = log.try_get_error_message(exception)
        self.assertEqual("", actual)

if __name__ == '__main__':
    unittest.main()

