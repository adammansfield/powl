#!/usr/bin/env python
"""Tests for TransactionAction in powl.action."""
import time
import unittest
from tests.mocks.filesystem import MockFile
from tests.mocks.parser import MockParser
from powl.transactionconverter import TransactionConverter
from powl.parser import TransactionParser

class TestTransactionConverter(unittest.TestCase):
    """Class for testing the transaction action."""

    _FILES = {
        "cash":       MockFile("./", "cash.qif"),
        "chequing":   MockFile("./", "chequing.qif"),
        "visa":       MockFile("./", "visa.qif"),
        "mastercard": MockFile("./", "mastercard.qif")
    }

    _ACCOUNT_TYPES = {
        "cash":       "Cash",
        "chequing":   "Bank",
        "visa":       "CCard",
        "mastercard": "CCard"
    }

    _ASSETS = {
        "cash":       "Assets:Cash",
        "chequing":   "Assets:Chequing",
        "savings":    "Assets:Savings"
        "portfolio":  "Assets:Portfolio"
    }
    _ASSETS_KEYS = _ASSETS.keys()

    _LIABILITIES = {
        "visa":       "Liabilities:Visa",
        "mastercard": "Liabilities:Mastercard",
        "loan":       "Liabilities:Loan",
        "payable":    "Liabilities:Payable"
    }
    _LIABILITIES = _LIABILITIES.keys()

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
        self._log = NullLogWriter()

        self._converter = QifConverter(
            self._log,
            self._FILES,
            self._ACCOUNT_TYPES,
            self._ASSETS,
            self._LIABILITIES,
            self._REVENUES,
            self._EXPENSES)

    def test_convert(self):
        # TODO: put proper values here.
        string = "" # input
        date = ""   # time.struct_time

        self._parser.parse_retval = TransactionData(
            "", # debit
            "", # credit
            "", # amount
            "") # memo

        try:
            self._converter.do(string, date)
        except:
            self.fail("do raised an unexpected exception")

        # TODO: assert mockfile._append_line_data == expected

    def test_invalid_key_to_file(self):
        # TODO: check to make sure that:
        #         1. each key in filenames exists as a key in accounts
        #         2. each key in account_types exists as a key in accounts
        #       else throw a KeyValue Error and write a test for this
        pass

    # Convert amount tests.
    def test_convert_amount_invalid_debit_account(self):
        """Test for an debit accounts that are invalid and do not exist."""
        valid_amount = "10.00"

        invalid_debit = "non-existant account"
        with self.assertRaises(KeyError) as context:
            self._converter._convert_amount(invalid_debit, valid_amount)
        self.assertEqual(
            context.exception.message,
            "account ({0}) does not exist".format(invalid_debit))

    def test_convert_amount_invalid_amount(self):
        """Test for amounts that cannot be converted to float."""
        valid_debit = self._ASSETS_KEYS[0]

        invalid_amount = "foo"
        with self.assertRaises(ValueError) as context:
            self._converter._convert_amount(valid_debit, invalid_amount)
        self.assertEqual(
            context.exception.message,
            "amount ({0}) cannot be converted to float".format(invalid_amount))

        invalid_amount = "5.01a"
        with self.assertRaises(ValueError) as context:
            self._converter._convert_amount(valid_debit, invalid_amount)
        self.assertEqual(
            context.exception.message,
            "amount ({0}) cannot be converted to float".format(invalid_amount))

    def test_convert_amount_debit_is_expense(self):
        """Test for output amount when debit is an expense."""
        debit = self._EXPENSES_KEYS[0]
        amount = "25.15"
        expected = "-25.15"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    def test_convert_amount_debit_is_not_expense(self):
        """Test for output amount when debit is not an expense."""
        debit = self._ASSETS_KEYS[0]
        amount = "10.75"
        expected = "10.75"
        actual = self._converter._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    def test_convert_amount_output_is_two_decimal_places(self):
        """Test various inputs that output is two decimal places."""
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
    def test_convert_date_type_error(self):
        """Test for a dates that are invalid."""
        date = "invalid date type"
        with self.assertRaises(TypeError) as context:
            self._converter._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because argument must be 9-item sequence, not str")

    def test_convert_date_overflow_error(self):
        """Test for a date that cannot be converted to C long."""
        date = (9999999999,0,0,0,0,0,0,0,0)
        with self.assertRaises(OverflowError) as context:
            self._converter._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because Python int too large to convert to C long")

    def test_convert_date_value_error(self):
        """Test for a date that is out of range."""
        date = (1000,0,0,0,0,0,0,0,0)
        with self.assertRaises(ValueError) as context:
            self._converter._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because year out of range")

    def test_convert_date_current_date(self):
        """Test the expected output using the current date."""
        date = localtime()
        expected = time.strftime("%m/%d/%Y", date)
        actual = self._converter._convert_date(date)
        self.assertEqual(actual, expected)

    def test_convert_date_past_date(self):
        """Test the expected output using a past date."""
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

    ## GET QIF FILE

    ## GET TRANSFER ACCOUNT

