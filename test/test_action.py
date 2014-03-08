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
    def test_convert_amount_invalid_account(self):
        """Test for an account that does not exist."""
        debit = "non-existant account"
        amount = "10.00"
        with self.assertRaises(KeyError) as context:
            self._action._convert_amount(debit, amount)
        self.assertEqual(
            context.exception.message,
            "account ({0}) does not exist".format(debit))

    def test_convert_amount_invalid_amount(self):
        """Test for an amount that cannot be converted to float."""
        debit = self._ASSETS_KEYS[0]
        amount = "foo"
        with self.assertRaises(ValueError) as context:
            self._action._convert_amount(debit, amount)
        self.assertEqual(
            context.exception.message,
            "amount ({0}) cannot be converted to float".format(amount))
    
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

        amount = "100.455"
        expected = "100.45"
        actual = self._action._convert_amount(debit, amount)
        self.assertEqual(actual, expected)
        
        amount = "100.456"
        expected = "100.46"
        actual = self._action._convert_amount(debit, amount)
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

