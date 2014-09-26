#!/usr/bin/env python
"""Tests for powl.log."""
import unittest
from powl import log

class TestTryGetErrorMessage(unittest.TestCase):
    """
    Class for testing get_error_message().
    """

    def test_returns_error_message(self):
        """
        Test to ensure it will return the message in the exception.
        """
        message = log.ErrorMessage("error message")
        exception = Exception()
        exception.args += (message,)
        actual = log.try_get_error_message(exception)
        self.assertEqual(str(message), actual)

    def test_does_not_throw_if_no_error_message(self):
        """
        Test to ensure that empty ErrorMessage is returned if none found.
        """
        exception = Exception()
        actual = log.try_get_error_message(exception)
        self.assertEqual("", actual)

if __name__ == '__main__':
    unittest.main()

