#!/usr/bin/env python
"""Tests for TransactionProcessor.py."""
import os
import sys
import time
import unittest
from Processors import TransactionProcessor

class TransactionTests(unittest.TestCase):
    """Class for testing transaction processing."""

    # VALIDITY
    def test_validity_accounts_bothvalid(self):
        """Test accounts validity with two valid accounts."""
        debit = 'ent'
        credit = 'c'
        expected = True
        actual = self.transaction.valid_accounts(debit, credit)
        self.assertEqual(actual, expected)

    def test_validity_accounts_onevalid(self):
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

    def test_validity_file_bothvalid(self):
        """Test file validity with both valid files."""
        debit = 'c'
        credit = 'a'
        expected = True
        actual = self.transaction.valid_file(debit, credit)
        self.assertEqual(actual, expected)

    def test_validity_file_onevalid(self):
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
    # TODO: expand conversion into separate tests
    def test_convert_date(self):
        """Test date conversion with samples."""
        datefmt='%Y-%m-%d'
        samples = [ (time.strptime('2010-03-01', datefmt), '03/01/2010'),
                    (time.strptime('2011-11-12', datefmt), '11/12/2011'),
                    (time.strptime('2012-01-15', datefmt), '01/15/2012'),
                    (time.strptime('2013-05-21', datefmt), '05/21/2013'),
                    (time.strptime('2014-08-09', datefmt), '08/09/2014'),
                    (time.strptime('2015-12-28', datefmt), '12/28/2015') ]
        for date, expected in samples:
            actual = self.transaction.qif_convert_date(date)
            self.assertEqual(actual, expected)

    def test_convert_filename(self):
        """Test filename conversion with samples."""
        samples = [ ('n', 'mis', 'chequing.qif'),
                    ('m', 'ear', 'mastercard.qif'),
                    ('ent', 'c', 'cash.qif'),
                    ('din', 'v', 'visa.qif'),
                    ('p', 'c', 'payable.qif'),
                    ('r', 'n', 'receivable.qif') ]
        for debit, credit, expected in samples:
            actual = self.transaction.qif_convert_filename(debit, credit)
            self.assertEqual(actual, expected)

    def test_convert_amount(self):
        """Test conversion of amount with samples."""
        samples = [ ('c', '4.28', '4.28'),
                    ('n', '9.12', '9.12'),
                    ('ent', '1.23', '-1.23'),
                    ('din', '1.23', '-1.23') ]
        for debit, amount, expected in samples:
            actual = self.transaction.qif_convert_amount(debit, amount)
            self.assertEqual(actual, expected)

    # INITIALIZATION
    def setUp(self):
        # TODO: replace paths with mock files
        # TODO: pass mock files setting accounts into constructor
        # TODO: set accounts in transactionprocessor before testing
        self.transaction = TransactionProcessor.\
                           TransactionProcessor()


if __name__ == '__main__':
    unittest.main()
