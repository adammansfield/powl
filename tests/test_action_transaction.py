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

    _LIABILITIES = {
        "visa":       "Liabilities:Visa",
        "mastercard": "Liabilities:Mastercard",
        "loan":       "Liabilities:Loan",
        "payable":    "Liabilities:Payable"
    }

    _REVENUES = {
        "earnings":   "Revenue:Earnings",
        "interest":   "Revenue:Interest",
        "capgain":    "Revenue:Capital Gains",
        "dividends":  "Revenue:Dividends"
    }

    _EXPENSES = {
        "food":       "Expenses:Food",
        "rent":       "Expenses:Rent",
        "utilities":  "Expenses:Utilities"
    }

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
    
    # TEST ACTION
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
            
    # CONVERT AMOUNT
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
        debit = _expenses.keys()[0]
        amount = 5.0
        with self.assertRaises(KeyError) as context:
            self.transaction._convert_amount(debit, amount)
        self.assertEqual(
            context.exception.message,
            "account ({0}) does not exist".format(debit))





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

