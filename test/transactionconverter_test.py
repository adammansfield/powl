#!/usr/bin/env python
"""Tests for TransactionAction in powl.action."""
import time
import unittest
from powl.transactionconverter import QifConverter
from test.mock.filesystem import MockFile
from test.mock.logwriter import MockLogWriter
from test.mock.parser import MockParser

class TestTransactionConverter(unittest.TestCase):
    """
    Class for testing the transaction action.
    """

    _FILES = {
        "cash":       MockFile("./", "cash.qif"),
        "chequing":   MockFile("./", "chequing.qif"),
        "visa":       MockFile("./", "visa.qif"),
        "mastercard": MockFile("./", "mastercard.qif")
    }
    _FILES_KEYS = _FILES.keys()

    _ACCOUNT_TYPES = {
        "cash":       "Cash",
        "chequing":   "Bank",
        "visa":       "CCard",
        "mastercard": "CCard"
    }
    _ACCOUNT_TYPES_KEYS = _ACCOUNT_TYPES.keys()

    _ASSETS = {
        "cash":       "Assets:Cash",
        "chequing":   "Assets:Chequing",
        "savings":    "Assets:Savings",
        "portfolio":  "Assets:Portfolio"
    }
    _ASSETS_KEYS = _ASSETS.keys()

    _LIABILITIES = {
        "visa":       "Liabilities:Visa",
        "mastercard": "Liabilities:Mastercard",
        "loan":       "Liabilities:Loan",
        "payable":    "Liabilities:Payable"
    }
    _LIABILITIES_KEYS = _LIABILITIES.keys()

    _REVENUES = {
        "earnings":   "Revenue:Earnings",
        "interest":   "Revenue:Interest",
        "capgain":    "Revenue:Capital Gains",
        "dividends":  "Revenue:Dividends"
    }
    _REVENUES_KEYS = _REVENUES.keys()

    _EXPENSES = {
        "food":       "Expenses:Food",
        "rent":       "Expenses:Rent",
        "utilities":  "Expenses:Utilities"
    }
    _EXPENSES_KEYS = _EXPENSES.keys()

    def setUp(self):
        self._log = MockLogWriter()

        self._converter = QifConverter(
            self._log,
            self._FILES,
            self._ACCOUNT_TYPES,
            self._ASSETS,
            self._LIABILITIES,
            self._REVENUES,
            self._EXPENSES)

    # Convert whole transaction tests.
    @unittest.skip("TODO: impl")
    def test__convert(self):
        date = None
        debit = ""
        credit = ""
        amount = ""
        memo = ""

        actual_record, actual_file = self._converter.convert(
            date,
            debit,
            credit,
            amount,
            memo)

        self.assertEqual(actual_record, "")
        self.assertEqual(actual_file, None)

    # Format QIF record tests.
    def test__format_qif_record__expected_output(self):
    # TODO: test expected output.
        pass

    # Convert amount tests.
    def test__convert_amount__invalid_debit_account(self):
        """
        Test for a debit account that is invalid and does not exist.
        """
        debit = "non-existant account"
        amount = "10.00"
        with self.assertRaises(KeyError) as context:
            self._converter._convert_amount(debit, amount)
        self.assertEqual(
            context.exception.message,
            "account key ({0}) does not exist".format(debit))

    def test__convert_amount__invalid_amount(self):
        """
        Test for an amount that cannot be converted to float.
        """
        debit = self._ASSETS_KEYS[0]
        amount = "5.01a"
        with self.assertRaises(ValueError) as context:
            self._converter._convert_amount(debit, amount)
        self.assertEqual(
            context.exception.message,
            "amount ({0}) cannot be converted to float".format(amount))

    def test__convert_amount__debit_is_expense(self):
        """
        Test for output amount when debit is an expense.
        """
        debit = self._EXPENSES_KEYS[0]
        amount = "25.15"
        expected = "-25.15"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    def test__convert_amount__debit_is_not_expense(self):
        """
        Test for output amount when debit is not an expense.
        """
        debit = self._ASSETS_KEYS[0]
        amount = "10.75"
        expected = "10.75"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    def test__convert_amount__output_is_two_decimal_places(self):
        """
        Test various inputs that output is two decimal places.
        """
        debit = self._ASSETS_KEYS[0]

        amount = "5"
        expected = "5.00"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

        amount = "10.2"
        expected = "10.20"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

        amount = "20.45"
        expected = "20.45"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

        amount = "100.4550"
        expected = "100.45"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

        amount = "100.4551"
        expected = "100.46"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    # Convert date tests.
    def test__convert_date__type_error(self):
        """
        Test for a date that is invalid.
        """
        date = "invalid date type"
        with self.assertRaises(TypeError) as context:
            self._converter._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because argument must be 9-item sequence, not str")

    def test__convert_date__overflow_error(self):
        """
        Test for a date that cannot be converted to C long.
        """
        date = (9999999999,0,0,0,0,0,0,0,0)
        with self.assertRaises(OverflowError) as context:
            self._converter._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because Python int too large to convert to C long")

    def test__convert_date__value_error(self):
        """
        Test for a date that is out of range.
        """
        date = (1000,0,0,0,0,0,0,0,0)
        with self.assertRaises(ValueError) as context:
            self._converter._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because year out of range")

    def test__convert_date__current_date(self):
        """
        Test the expected output using the current date.
        """
        date = time.localtime()
        expected = time.strftime("%m/%d/%Y", date)
        actual = self._converter._convert_date(date)
        self.assertEqual(actual, expected)

    def test__convert_date__past_date(self):
        """
        Test the expected output using a past date.
        """
        date = time.gmtime(0)
        expected = "01/01/1970"
        actual = self._converter._convert_date(date)
        self.assertEqual(actual, expected)

    # TODO: for both get_file and get_transfer:
    #           - invalid debit
    #           - invalid credit
    #           - invalid debit and invalid credit
    #           - debit with matching file and credit without matching file
    #           - debit without matching file and credit with matching file
    #           - debit without matching file and credit without matching file
    #
    # TODO: add test using get_file and get_transfer together to make sure
    #       that both returns work together eg. file from debit then transfer
    #       must be from credit and vice versa.

    # Get QIF file tests
    def test__get_qif_file__both_have_no_file(self):
        """
        Test for a invalid debit key (that has no associated file) and an
        invalid credit key (that has no associated file).
        """
        debit = "invalid debit key"
        credit = "invalid credit key"
        with self.assertRaises(KeyError) as context:
            self._converter._get_qif_file(debit, credit)
        expected_message = (
            "neither debit key ({0}) ".format(debit) +
            "or credit key ({0}) ".format(credit) +
            "has an associated QIF file")
        self.assertEqual(context.exception.message, expected_message)

    def test__get_qif_file__both_have_file(self):
        """
        Test for a valid debit key (that has an associated file) and a valid
        credit key (that has an associated file). Expect back the file
        associated with the debit key since it has higher priority.
        """
        debit = self._FILES_KEYS[0]
        credit = self._FILES_KEYS[1]
        expected = self._FILES[debit]
        actual = self._converter._get_qif_file(debit, credit)
        self.assertEqual(actual, expected)

    def test__get_qif_file__debit_has_file_and_credit_has_no_file(self):
        """
        Test for a valid debit key (that has an associated file) and an
        invalid credit key (that has no associated file).
        """
        debit = self._FILES_KEYS[0]
        credit = "invaild key"
        expected = self._FILES[debit]
        actual = self._converter._get_qif_file(debit, credit)
        self.assertEqual(actual, expected)

    def test__get_qif_file__debit_has_no_file_and_credit_has_file(self):
        """
        Test for a invalid debit key (that has no associated file) and a
        valid credit (that has an associated file).
        """
        debit = "invalid key"
        credit = self._FILES_KEYS[1]
        expected = self._FILES[credit]
        actual = self._converter._get_qif_file(debit, credit)
        self.assertEqual(actual, expected)

    ## Get QIF transfer account tests
    #def test__get_transfer__both_file_both_account(self):
    #    """
    #    Test for debit and credit keys that both have have associated QIF
    #    files and associated QIF accounts.
    #    """

if __name__ == '__main__':
    unittest.main(verbosity=2)
