#!/usr/bin/env python
"""Tests for powl.log."""
import unittest
from powl import exception

class TestErrorMessageFunctions(unittest.TestCase):
    """
    Class for testing get_error_message().
    """

    def test__add__sanity(self):
        """
        Test that added message by string can be retrieved.
        """
        error_message = "error message"
        err = Exception()
        exception.add_message(err, error_message)
        actual = exception.get_message(err)
        self.assertEqual(error_message, actual)

    def test__create__first_arg_is_message_preceded_by_type(self):
        """
        Test that the first argument is input message preceded by <type>:.
        """
        exception_type = ValueError
        input_message = "this is an error message"
        expected_message = ("{0}: {1}".format(exception_type.__name__,
                                              input_message))
        err = exception.create(exception_type, input_message)
        actual_message = err.args[0]
        self.assertEqual(expected_message, actual_message)

    def test__create__return_is_input_type(self):
        """
        Test that the returned exception is the correct type.
        """
        exception_type = ValueError
        err = exception.create(exception_type, "")
        self.assertEqual(exception_type, type(err))

    def test__get__does_not_throw_if_no_error_message(self):
        """
        Test to ensure that empty ErrorMessage is returned if none found.
        """
        err = Exception()
        actual = exception.get_message(err)
        self.assertEqual("", actual)

if __name__ == '__main__':
    unittest.main()

