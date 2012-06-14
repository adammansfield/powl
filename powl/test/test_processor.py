#!/usr/bin/env python
import os
import sys
import unittest
from powl.processor import Processor

class ProcessorTest(unittest.TestCase):

    def setUp(self):
        self.processor = Processor()

    # MESSAGE PARSING
    def test_parse_message_bodycomposition(self):
        """Test the message parser with a body composition message."""
        message = 'bodycomposition -m 200 -f 15.0'
        expected = self.processor.action_bodycomposition
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_event(self):
        """Test the message parser with an event message."""
        message = 'event 5pm coffee'
        expected = self.processor.action_event
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_nomatch(self):
        """Test the message parser with a message without an action."""
        message = 'blah this message is blank'
        expected = self.processor.action_nomatch
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_note(self):
        """Test the message parser with a note message."""
        message = 'note coffee is great'
        expected = self.processor.action_note
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_todo(self):
        """Test the message parser with a todo message."""
        message = 'todo buy coffee'
        expected = self.processor.action_todo
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_transaction(self):
        """Test the message parser with a transaction message."""
        message = 'transaction -d mis -c c -a 5 -m coffee'
        expected = self.processor.action_transaction
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
