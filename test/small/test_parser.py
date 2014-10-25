#!/usr/bin/env python
import unittest
from powl import actiontype
from powl import exception
from powl import parser

class ActionItemParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = parser.ActionItemParser()

    def test__parse__bodycomposition__key_is_b(self):
        """
        Test with string for a body composition action.
        """
        string = "b -m 136 -f 13.5"
        expected_action_key = actiontype.BODY_COMPOSITION
        expected_data = "-m 136 -f 13.5"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__bodycomposition__key_is_bodycomposition(self):
        """
        Test with string for a body composition action.
        """
        string = "bodycomposition -m 200 -f 15.0"
        expected_action_key = actiontype.BODY_COMPOSITION
        expected_data = "-m 200 -f 15.0"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__note__key_is_n(self):
        """
        Test with string for a note action.
        """
        string = "n buy some coffee"
        expected_action_key = actiontype.NOTE
        expected_data = "buy some coffee"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__note__key_is_note(self):
        """
        Test with string for a note action.
        """
        string = "note coffee is great"
        expected_action_key = actiontype.NOTE
        expected_data = "coffee is great"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__transaction__key_is_a(self):
        """
        Test with string for a transaction action.
        """
        string = "a -d out -c debitcard -a 10 -m dinner"
        expected_action_key = actiontype.TRANSACTION
        expected_data = "-d out -c debitcard -a 10 -m dinner"
        actual_action_key, actual_data = self.parser.parse(string)
        self.assertEqual(expected_action_key, actual_action_key)
        self.assertEqual(expected_data, actual_data)

    def test__parse__transaction__key_is_transaction(self):
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
        expected_message = "action key (write) is unknown"
        with self.assertRaises(KeyError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)


class BodyCompositionDataFlagParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = parser.BodyCompositionDataFlagParser()

    def test__parse__fat_percentage_is_not_a_number(self):
        """
        Test for string where mass is not a number.
        """
        string = "-m 200 -f 1i5.2"
        expected_message = "fat percentage (1i5.2) is not a number"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__mass_is_not_a_number(self):
        """
        Test for string where mass is not a number.
        """
        string = "-m 200a -f 15.2"
        expected_message = "mass (200a) is not a number"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_fat_percentage(self):
        """
        Test for string missing fat percentage value.
        """
        string = "-m 100"
        expected_message = ("fat percentage was not parsed "
                            "from ({0})".format(string))
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_mass(self):
        """
        Test for string missing mass value.
        """
        string = "-f 10.1"
        expected_message = "mass was not parsed from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__sanity(self):
        """
        Test for expected mass and fat percentage.
        """
        string = "-m 200.1 -f 15.2"
        expected_mass = "200.1"
        expected_fat_percentage = "15.2"
        actual = self.parser.parse(string)
        self.assertEqual(expected_mass, actual.mass)
        self.assertEqual(expected_fat_percentage, actual.fat_percentage)


class BodyCompositionDataPositionalParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = parser.BodyCompositionDataPositionalParser()

    def test__parse__fat_percentage_is_not_a_number(self):
        """
        Test for string where fat percentage is not a number.
        """
        string = "200 1i5.2"
        expected_message = "fat percentage (1i5.2) is not a number"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__mass_is_not_a_number(self):
        """
        Test for string where mass is not a number.
        """
        string = "200a 15.2"
        expected_message = "mass (200a) is not a number"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_all_values(self):
        """
        Test for string missing all values.
        """
        string = ""
        expected_message = "not enough arguments from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_one_value(self):
        """
        Test for string missing one value.
        """
        string = "150"
        expected_message = "not enough arguments from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__sanity(self):
        """
        Test for expected mass and fat percentage.
        """
        string = "200.1 15.2"
        expected_mass = 200.1
        expected_fat_percentage = 15.2
        actual = self.parser.parse(string)
        self.assertEqual(expected_mass, actual.mass)
        self.assertEqual(expected_fat_percentage, actual.fat_percentage)


class TransactionDataFlagParser(unittest.TestCase):

    def setUp(self):
        self.parser = parser.TransactionDataFlagParser()

    def test__parse__memo_multiple_words_with_quotes(self):
        """Test transaction parser for expected memo of multiple words."""
        string = "-d con -c ps -a 250 -m \"bought contacts\""
        expected = "bought contacts"
        data = self.parser.parse(string)
        self.assertEqual(expected, data.memo)

        debit = "con"
        credit = "pc"
        amount = "250"
        memo = "purchased contacts"
        string = "-d {0} -c {1} -a {2} -m \"{3}\"".format(debit, credit,
                                                          amount, memo)
        actual = self.parser.parse(string)
        self.assertEqual(debit, actual.debit)
        self.assertEqual(credit, actual.credit)
        self.assertEqual(amount, actual.amount)
        self.assertEqual(memo, actual.memo)

    def test__parse__amount_is_not_a_number(self):
        """
        Test that the method throws when amount is not a number.
        """
        amount = "35b"
        string = "-d phone -c bank -a {0} -m bill".format(amount)
        expected_message = "amount ({0}) is not a number".format(amount)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_amount(self):
        """
        Test that the method throws if string is missing amount flag.
        """
        string = "-d phone -c bank -m bill"
        expected_message = "amount is missing from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_debit(self):
        """
        Test that the method throws if string is missing debit flag.
        """
        string = "-c bank -a 5 -m bill"
        expected_message = "debit is missing from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_credit(self):
        """
        Test that the method throws if string is missing credit flag.
        """
        string = "-d phone -a 5 -m bill"
        expected_message = "credit is missing from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_memo(self):
        """
        Test that the method throws if string is missing memo flag.
        """
        string = "-d phone -c bank -a 5"
        expected_message = "memo is missing from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__sanity(self):
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


class TransactionDataPositionalParser(unittest.TestCase):

    def setUp(self):
        self.parser = parser.TransactionDataPositionalParser()

    def test__parse__amount_is_not_a_number(self):
        """
        Test that the method throws when amount is not a number.
        """
        amount = "35b"
        string = "{0} phone bank phone bill".format(amount)
        expected_message = "amount ({0}) is not a number".format(amount)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__memo_multiple_words(self):
        """
        Test transaction parser for expected memo of multiple words.
        """
        string = "250 con pc bought contacts"
        expected = "bought contacts"
        data = self.parser.parse(string)
        self.assertEqual(expected, data.memo)

    def test__parse__missing_all_values(self):
        """
        Test for string missing all values
        """
        string = ""
        expected_message = "not enough arguments from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_one_value(self):
        """
        Test for string missing one value.
        """
        string = "5.25 coffee debitcard"
        expected_message = "not enough arguments from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_two_values(self):
        """
        Test for string missing one value.
        """
        string = "5.25 coffee"
        expected_message = "not enough arguments from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__missing_three_values(self):
        """
        Test for string missing one value.
        """
        string = "5.25"
        expected_message = "not enough arguments from ({0})".format(string)
        with self.assertRaises(ValueError) as context:
            self.parser.parse(string)
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__parse__sanity(self):
        """
        Test with sample data for expected output.
        """
        debit = "mis"
        credit = "ca"
        amount = "5.25"
        memo = "coffee"
        string = "{0} {1} {2} {3}".format(amount, debit, credit, memo)
        actual = self.parser.parse(string)
        self.assertEqual(debit, actual.debit)
        self.assertEqual(credit, actual.credit)
        self.assertEqual(amount, actual.amount)
        self.assertEqual(memo, actual.memo)


if __name__ == '__main__':
    unittest.main()

