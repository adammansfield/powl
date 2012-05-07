#!/usr/bin/env python
"""Tests for TransactionProcessor.py."""
import os
import sys
import time
import unittest
from powl.processors.transaction import Transaction

class TransactionTests(unittest.TestCase):
    """Class for testing transaction processing."""

    # VALIDITY
    ## ACCOUNTS
    def test_validity_accounts_bothvalid(self):
        """Test accounts validity with two valid accounts."""
        debit = 'ent'
        credit = 'c'
        expected = True
        actual = self.transaction.valid_accounts(debit, credit)
        self.assertEqual(actual, expected)

    def test_validity_accounts_singlevalid(self):
        """Test accounts validity with only one valid account."""
        debit = 'din'
        credit = 'a'
        expected = False
        actual = self.transaction.valid_accounts(debit, credit)
        self.assertEqual(actual, expected)

    def test_validity_accounts_nonevalid(self):
        """Test accounts validity with no valid accounts."""
        debit = 'zbk'
        credit = 'k'
        expected = False
        actual = self.transaction.valid_accounts(debit, credit)
        self.assertEqual(actual, expected)

    ## AMOUNT
    def test_validity_amount_isnumber(self):
        """Test amount validity with a number."""
        amount = '25.01'
        expected = True
        actual = self.transaction.valid_amount(amount)
        self.assertEqual(actual, expected)

    def test_validity_amount_nan(self):
        """Test amount validity with not a number."""
        amount = '4.hf'
        expected = False
        actual = self.transaction.valid_amount(amount)
        self.assertEqual(actual, expected)

    ## DATE
    def test_validity_date_failure(self):
        """Test date validity with an invalid date."""
        date = 'not a date!'
        expected = False
        actual = self.transaction.valid_date(date)
        self.assertEqual(actual, expected)
    
    def test_validity_date_success(self):
        """Test date validity with a valid date."""
        date = time.localtime()
        expected = True
        actual = self.transaction.valid_date(date)
        self.assertEqual(actual, expected)

    ## FILE
    def test_validity_file_bothvalid(self):
        """Test file validity with both valid files."""
        debit = 'c'
        credit = 'a'
        expected = True
        actual = self.transaction.valid_file(debit, credit)
        self.assertEqual(actual, expected)

    def test_validity_file_singlevalid(self):
        """Test file validity with one valid file."""
        debit = 'n'
        credit = 'int'
        expected = True
        actual = self.transaction.valid_file(debit, credit)
        self.assertEqual(actual, expected)

    def test_validity_file_nonevalid(self):
        """Test file validity with no valid files."""
        debit = 'k'
        credit = 'lik'
        expected = False
        actual = self.transaction.valid_file(debit, credit)
        self.assertEqual(actual, expected)

    # CONVERSION
    ## DATE
    def test_convert_date_currenttime(self):
        """Test date conversion using the current time."""
        current_date = time.localtime()
        expected = time.strftime('%m/%d/%Y', current_date)
        actual = self.transaction.qif_convert_date(current_date)
        self.assertEqual(actual, expected)

    def test_convert_date_sample(self):
        """Test date conversion with a sample."""
        sample = time.strptime('2015-03-14', '%Y-%m-%d')
        expected = '03/14/2015'
        actual = self.transaction.qif_convert_date(sample)
        self.assertEqual(actual, expected)

    ## FILENAME
    def test_convert_filename_bothfiles(self):
        """Test filename conversion with two valid files."""
        debit = 'm'
        credit = 'n'
        expected = 'mastercard.qif'
        actual = self.transaction.qif_convert_filename(debit, credit)
        self.assertEqual(actual, expected)

    def test_convert_filename_singlefile(self):
        """Test filename conversion with one valid file."""
        debit = 'ent'
        credit = 'c'
        expected = 'cash.qif'
        actual = self.transaction.qif_convert_filename(debit, credit)
        self.assertEqual(actual, expected)

    ## AMOUNT
    def test_convert_amount_regular(self):
        """Test filename conversion with one valid file."""
        debit = 'int'
        amount = '2.13'
        expected = '2.13'
        actual = self.transaction.qif_convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    def test_convert_amount_expense(self):
        """Test filename conversion with one valid file."""
        debit = 'ent'
        amount = '2.13'
        expected = '-2.13'
        actual = self.transaction.qif_convert_amount(debit, amount)
        self.assertEqual(actual, expected)

    # INITIALIZATION
    def setUp(self):
        # TODO: set accounts in transactionprocessor before testing
        self.transaction = Transaction()


if __name__ == '__main__':
    unittest.main()
