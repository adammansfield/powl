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
        message = "bodycomposition -m 200 -f 15.0"
        expected = self.processor.action_bodycomposition
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_event(self):
        """Test the message parser with an event message."""
        message = "event 5pm coffee"
        expected = self.processor.action_event
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_nomatch(self):
        """Test the message parser with a message without an action."""
        message = "blah this message is blank"
        expected = self.processor.action_nomatch
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_note(self):
        """Test the message parser with a note message."""
        message = "note coffee is great"
        expected = self.processor.action_note
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_todo(self):
        """Test the message parser with a todo message."""
        message = "todo buy coffee"
        expected = self.processor.action_todo
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    def test_parse_message_transaction(self):
        """Test the message parser with a transaction message."""
        message = "transaction -d mis -c c -a 5 -m coffee"
        expected = self.processor.action_transaction
        actual, data = self.processor.parse_message(message)
        self.assertEqual(expected, actual)

    # TRANSACTION PARSING
    def test_parse_transaction_debit(self):
        """Test transaction parser for expected debit."""
        data = "-d mis -c ca -a 5 -m coffee"
        expected = 'mis'
        actual, credit, amount, memo = self.processor.parse_transaction(data)
        self.assertEqual(expected, actual)
        
    def test_parse_transaction_credit(self):
        """Test transaction parser for expected credit."""
        data = "-d ent -c lm -a 2 -m timbit"
        expected = 'lm'
        debit, actual, amount, memo = self.processor.parse_transaction(data)
        self.assertEqual(expected, actual)

    def test_parse_transaction_amount(self):
        """Test transaction parser for expected amount."""
        data = "-d out -c lv -a 25 -m dinner"
        expected = '25'
        debit, credit, actual, memo = self.processor.parse_transaction(data)
        self.assertEqual(expected, actual)

    def test_parse_transaction_memo_one_word_no_quote(self):
        """Test transaction parser for expected memo of one word."""
        data = "-d mai -c pc -a 1 -m timbit"
        expected = 'timbit'
        debit, credit, amount, actual = self.processor.parse_transaction(data)
        self.assertEqual(expected, actual)

    def test_parse_transaction_memo_one_word_with_quote(self):
        """Test transaction parser for expected memo of one word."""
        data = "-d mai -c pc -a 1 -m \"timbit\""
        expected = 'timbit'
        debit, credit, amount, actual = self.processor.parse_transaction(data)
        self.assertEqual(expected, actual)

    def test_parse_transaction_memo_multiple_words(self):
        """Test transaction parser for expected memo of multiple words."""
        data = "-d con -c ps -a 250 -m \"bought contacts\""
        expected = 'bought contacts'
        debit, credit, amount, actual = self.processor.parse_transaction(data)
        self.assertEqual(expected, actual)

    # BODY COMPOSITION PARSING
    def test_parse_bodycomposition_mass(self):
        """Test bodycomposition parser for expected mass."""
        data = "-m 200.1 -f 15.2"
        expected = '200.1'
        actual, fat = self.processor.parse_bodycomposition(data)
        self.assertEqual(expected, actual)

    def test_parse_bodycomposition_fat(self):
        """Test bodycomposition parser for expected fat percentage."""
        data = "-m 200.1 -f 15.2"
        expected = '15.2'
        mass, actual = self.processor.parse_bodycomposition(data)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
