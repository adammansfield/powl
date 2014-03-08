#!/usr/bin/env python
"""Tests for TransactionAction in powl.action."""
import unittest
from tests.mocks.filesystem import MockFile
from tests.mocks.parser import MockParser
from powl.action import TransactionAction
from powl.parser import TransactionParser

class TestActionTransaction(unittest.TestCase):
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

    # INITIALIZATION
    def setUp(self):
        # TODO: set accounts in transactionprocessor before testing
        self._log = NullLogWriter()
        self._parser = MockParser()

        self._action = Transaction(
            self._log,
            self._parser,
            self._FILES,
            self._ACCOUNT_TYPES,
            self._ASSETS,
            self._LIABILITIES,
            self._REVENUES,
            self._EXPENSES
        )
    
    # ACTION
    def test_do_valid(self):
        # TODO: put proper values here.
        string = "" # input
        date = ""   # time.struct_time

        self._parser.parse_retval = TransactionData(
            "", # debit
            "", # credit
            "", # amount
            "") # memo 

        try:
            self._action.do(string, date)
        except:
            self.fail("do raised an unexpected exception")

        # TODO: assert mockfile._append_line_data == expected
            
    # QIF CONVERSION
    ## CONVERT AMOUNT
    def test_convert_amount_invalid_debit_account(self):
        """Test for an debit accounts that are invalid and do not exist."""
        valid_amount = "10.00"

        invalid_debit = "non-existant account"
        with self.assertRaises(KeyError) as context:
            self._action._convert_amount(invalid_debit, valid_amount)
        self.assertEqual(
            context.exception.message,
            "account ({0}) does not exist".format(invalid_debit))

    def test_convert_amount_invalid_amount(self):
        """Test for amounts that cannot be converted to float."""
        valid_debit = self._ASSETS_KEYS[0]

        invalid_amount = "foo"
        with self.assertRaises(ValueError) as context:
            self._action._convert_amount(valid_debit, invalid_amount)
        self.assertEqual(
            context.exception.message,
            "amount ({0}) cannot be converted to float".format(invalid_amount))

        invalid_amount = "5.01a"
        with self.assertRaises(ValueError) as context:
            self._action._convert_amount(valid_debit, invalid_amount)
        self.assertEqual(
            context.exception.message,
            "amount ({0}) cannot be converted to float".format(invalid_amount))
    
    def test_convert_amount_debit_is_expense(self):
        """Test for output amount when debit is an expense."""
        debit = self._EXPENSES_KEYS[0] 
        amount = "25.15"
        expected = "-25.15"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    def test_convert_amount_debit_is_not_expense(self):
        """Test for output amount when debit is not an expense."""
        debit = self._ASSETS_KEYS[0] 
        amount = "10.75"
        expected = "10.75"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    def test_convert_amount_output_is_two_decimal_places(self):
        """Test various inputs that output is two decimal places."""
        debit = self._ASSETS_KEYS[0]

        amount = "5"
        expected = "5.00"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

        amount = "10.2"
        expected = "10.20"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

        amount = "20.45"
        expected = "20.45"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

        amount = "100.4550"
        expected = "100.45"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)
        
        amount = "100.4551"
        expected = "100.46"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    ## CONVERT DATE
    def test_convert_date_type_error(self):
        """Test for a dates that are invalid."""
        date = "invalid date type"
        with self.assertRaises(TypeError) as context:
            self._action._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because argument must be 9-item sequence, not str")

    def test_convert_date_overflow_error(self):
        """Test for a date that cannot be converted to C long."""
        date = (9999999999,0,0,0,0,0,0,0,0)
        with self.assertRaises(OverflowError) as context:
            self._action._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because Python int too large to convert to C long")

    def test_convert_date_value_error(self):
        """Test for a date that is out of range."""
        date = (1000,0,0,0,0,0,0,0,0)
        with self.assertRaises(ValueError) as context:
            self._action._convert_date(date)
        self.assertEqual(
            context.exception.message,
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because year out of range")

    def test_convert_date_current_date(self):
        """Test the expected output using the current date."""
        date = localtime()
        expected = time.strftime("%m/%d/%Y", date)
        actual = self._action.convert_date(date)
        self.assertEqual(actual, expected)

    def test_convert_date_past_date(self):
        """Test the expected output using a past date."""
        date = time.gmtime(0)
        expected = "01/01/1970"
        actual = self._action.convert_date(date)
        self.assertEqual(actual, expected)


    # VALIDITY
    ## ACCOUNTS
    def test_validity_account_exists(self):
        """Test for existing account."""
        try:
            self.transaction.validate_account("c")
            self.transaction.validate_account("mm")
            self.transaction.validate_account("int")
            self.transaction.validate_account("mis")
        except:
            self.fail("validate_account raised an unexpected exception")

    def test_validity_account_not_exist(self):
        """Test a not existing account."""
        account = "foobar"
        with self.assertRaises(ValueError) as context:
            self.transaction.validate_account(account)
        self.assertEqual(
            context.exception.message, "account does not exist")

    ## AMOUNT
    def test_validity_amount_valid(self):
        """Test a valid amount."""
        try:
            self.transaction.validate_amount(25)
            self.transaction.validate_amount(3.01)
            self.transaction.validate_amount("152.26")
        except:
            self.fail("validate_amount raised unexpected exception)

