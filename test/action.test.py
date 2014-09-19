#!/usr/bin/env python
"""Tests for powl.action."""
import sys
import time
import unittest
from powl import action
from powl import actiontype
from test.mock import action as mock_action
from test.mock import log as mock_log

class TestActionManager(unittest.TestCase):
    """
    Class for testing the ActionManager.
    """

    def setUp(self):
        self._log = mock_log.MockLog()
        self._action_manager = action.ActionManager(self._log)

    def test__do_action__action_is_called(self):
        """
        Test action was successfully added.
        """
        action_type = "mock action type"
        action_object = mock_action.MockAction()
        data = "sample data"
        date = time.localtime()

        self._action_manager.add_action(action_type, action_object)
        self._action_manager.do_action(action_type, data, date)
        self.assertTrue(action_object.do_called_with(data, date))

    def test__do_action__action_type_unknown(self):
        """
        Test for an action_type that is unknown.
        """
        action_type = "unknown action key"
        data = "sample data"
        date = time.localtime()

        expected_message = "action type ({0}) is unknown".format(action_type)
        with self.assertRaises(KeyError) as context:
            self._action_manager.do_action(action_type, data, date)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

if __name__ == '__main__':
    unittest.main()

