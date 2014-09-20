#!/usr/bin/env python
import unittest
from powl import actiontype
from powl import parser

class ActionItemParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = parser.ActionItemParser()

    def test__parse__bodycomposition(self):
        """
        Test with string for a body composition action.
        """
        string = "bodycomposition -m 200 -f 15.0"
        expected_action_key = actiontype.BODY_COMPOSITION
        expected_data = "-m 200 -f 15.0"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__note(self):
        """
        Test with string for a note action.
        """
        string = "note coffee is great"
        expected_action_key = actiontype.NOTE
        expected_data = "coffee is great"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__transaction(self):
        """
        Test with string for a transaction action.
        """
        string = "transaction -d mis -c c -a 5 -m coffee"
        expected_action_key = actiontype.TRANSACTION
        expected_data = "-d mis -c c -a 5 -m coffee"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__unknown_action(self):
        """
        Test with string for an unknown action.
        """
        string = "write this message"
        expected_message = "action key (write) is invalid"
        with self.assertRaises(KeyError) as context:
            self.parser.parse(string)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)


class BodyCompositionDataFlagParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = parser.BodyCompositionDataFlagParser()
        self.validate_called = False

    def test__parse__success(self):
        """
        Test for expected mass and fat percentage.
        """
        string = "-m 200.1 -f 15.2"
        expected_mass = "200.1"
        expected_fat_percentage = "15.2"
        actual = self.parser.parse(string)
        self.assertEqual(expected_mass, actual.mass)
        self.assertEqual(expected_fat_percentage, actual.fat_percentage)

    def test__parse__missing_fat_percentage(self):
        """
        Test for string missing fat percentage value.
        """
        string = "-m 100"
        expected_message = "fat percentage was not parsed from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_mass(self):
        """
        Test for string missing mass value.
        """
        string = "-f 10.1"
        expected_message = "mass was not parsed from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__parse__fat_percentage_is_not_a_number(self):
        """
        Test for string where mass is not a number.
        """
        string = "-m 200 -f 1i5.2"
        expected_message = "fat percentage is not a number (1i5.2)"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__parse__mass_is_not_a_number(self):
        """
        Test for string where mass is not a number.
        """
        string = "-m 200a -f 15.2"
        expected_message = "mass is not a number (200a)"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)


class TransactionDataFlagParser(unittest.TestCase):

    def setUp(self):
        self.parser = parser.TransactionDataFlagParser()

    def test__parse__success(self):
        """
        Test with sample data for expected output.
        """
        debit = "mis"
        credit = "ca"
        amount = "5.25"
        memo = "coffee"
        string = "-d {0} -c {1} -a {2} -m {3}".format(debit, credit, amount,
                                                      memo)
        actual = self.parser.parse(string)
        self.assertEqual(debit, actual.debit)
        self.assertEqual(credit, actual.credit)
        self.assertEqual(amount, actual.amount)
        self.assertEqual(memo, actual.memo)

    def test_parse_transaction_memo_one_word_no_quote(self):
        """Test transaction parser for expected memo of one word."""
        string = "-d mai -c pc -a 1 -m timbit"
        expected = "timbit"
        data = self.parser.parse(string)
        self.assertEqual(expected, data.memo)

    def test_parse_transaction_memo_one_word_with_quote(self):
        """Test transaction parser for expected memo of one word."""
        string = "-d mai -c pc -a 1 -m \"timbit\""
        expected = "timbit"
        data = self.parser.parse(string)
        self.assertEqual(expected, data.memo)

    def test_parse_transaction_memo_multiple_words(self):
        """Test transaction parser for expected memo of multiple words."""
        string = "-d con -c ps -a 250 -m \"bought contacts\""
        expected = "bought contacts"
        data = self.parser.parse(string)
        self.assertEqual(expected, data.memo)


class TransactionDataPositionalParser(unittest.TestCase):

    def setUp(self):
        self.parser = parser.TransactionDataPositionalParser()


if __name__ == '__main__':
    unittest.main()

