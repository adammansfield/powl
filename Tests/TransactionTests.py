#!/usr/bin/env python
"""Tests for TransactionProcessor.py."""
import datetime
import os
import sys
import time
import unittest
sys.path.append(os.path.dirname(os.getcwd()))
import TransactionProcessor

class TransactionTests(unittest.TestCase):
    """Class for testing transaction processing."""

    # VALIDITY
    def test_validity_empty(self):
        """Test validity for empty parameters."""
        expected = False
        actual = self.transaction.is_valid("", "")
        self.assertEqual(actual, expected)

    def test_validity_samples(self):
        """Test validity based on preset accounts."""
        samples = [ ('ent', 'c', True),
                    ('din', 'm', True),
                    ('gas', 'v', True),
                    ('bka', 'a', False),
                    ('lyg', 'm', False),
                    ('ent', 'k', False) ]
        for debit, credit, expected in samples:
            actual = self.transaction.is_valid(debit, credit)
            self.assertEqual(actual, expected)

    # CONVERSION
    def test_convert_date_samples(self):
        """Test date conversion with samples."""
        datefmt = '%Y-%m-%d'
        samples = [ (time.strptime('2010-03-01', datefmt), '03/01/2010'),
                    (time.strptime('2011-11-12', datefmt), '11/12/2011'),
                    (time.strptime('2012-01-15', datefmt), '01/15/2012'),
                    (time.strptime('2013-05-21', datefmt), '05/21/2013'),
                    (time.strptime('2014-08-09', datefmt), '08/09/2014'),
                    (time.strptime('2015-12-28', datefmt), '12/28/2015') ]
        for date, expected in samples:
            actual = self.transaction.qif_convert_date(date)
            self.assertEqual(actual, expected)

    def test_convert_filename_samples(self):
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

    def test_convert_amount_samples(self):
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
