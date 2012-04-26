#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.getcwd()))
import TransactionProcessor

class TransactionTests(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.dirname(os.getcwd()))
        # TODO: replace paths with mock files
        # TODO: pass mock files setting accounts into constructor
        self.transaction = TransactionProcessor.\
                           TransactionProcessor("","","")

    def test_validity_empty(self):
        """Test validity for empty parameters."""
        expected = False
        actual = self.transaction.is_valid("", "")
        self.assertEqual(expected, actual)

    def test_validity_samples(self):
        """Test validity based on preset accounts."""
        # TODO: set accounts in transactionprocessor before testing
        samples = [ ('ent', 'c', True),
                    ('din', 'm', True),
                    ('gas', 'v', True),
                    ('bka', 'a', False),
                    ('lyg', 'm', False),
                    ('ent', 'k', False) ]
        for debit, credit, expected in samples:
            actual = self.transaction.is_valid(debit, credit)
            self.assertEqual(expected, actual)

    #def test_sample(self):
    #    # TODO: get current date time for testing
    #    date = 
    #    debit = 'ent'
    #    credit = 'm'
    #    amount = '-5.23'
    #    memo = 'test transaction'
    #    expected = ("D{0}{1}".format(date, os.linesep) +
    #                "T{0}{1}".format(amount, os.linesep) +
    #                "L{0}{1}".format(transfer, os.linesep) +
    #                "M{0}{1}".format(memo, os.linesep) +
    #                "^{0}".format(os.linesep))
    #    actual = self.transaction.Process(date, debit, credit, amount, memo)
    #    self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
