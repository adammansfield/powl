#!/usr/bin/env python
"""Tests for powl.transactionconverter."""
import textwrap
import time
import unittest
from powl import transactionconverter
from test.mock import filesystem
from test.mock import log

class TestQifConverter(unittest.TestCase):
    """
    Class for testing the QifConverter.
    """

    def setUp(self):
        self._FILES = {
            "cash":       filesystem.MockFile("./", "cash.qif"),
            "chequing":   filesystem.MockFile("./", "chequing.qif")}

        self._ACCOUNT_TYPES = {
            "cash":       "Cash",
            "chequing":   "Bank"}

        self._ASSETS = {
            "cash":       "Assets:Cash",
            "chequing":   "Assets:Chequing"}

        self._LIABILITIES = {
            "visa":       "Liabilities:Visa",
            "mastercard": "Liabilities:Mastercard"}

        self._REVENUES = {
            "earnings":   "Revenue:Earnings",
            "interest":   "Revenue:Interest"}

        self._EXPENSES = {
            "food":       "Expenses:Food",
            "utilities":  "Expenses:Utilities"}

        self._ACCOUNTS = dict(
            self._ASSETS.items() +
            self._LIABILITIES.items() +
            self._REVENUES.items() +
            self._EXPENSES.items())

        self._ACCOUNTS_WITHOUT_FILE = {
            k:v for k,v in self._ACCOUNTS.items()
            if k not in self._FILES.keys()}

        self._log = log.MockLog()

        self._converter = transactionconverter.QifConverter(
            self._log,
            self._FILES,
            self._ACCOUNT_TYPES,
            self._ASSETS,
            self._LIABILITIES,
            self._REVENUES,
            self._EXPENSES)

    # convert() tests.
    def test__convert(self):
        date = time.localtime()
        debit = self._EXPENSES.keys()[0]
        credit = self._FILES.keys()[0]
        amount = "5.25"
        memo = "purchased supplies"

        qif_date = time.strftime("%m/%d/%Y", date)
        qif_amount = "-5.25"
        qif_transfer = self._EXPENSES[debit]

        expected_file = self._FILES[credit]
        expected_record = textwrap.dedent(
            """\
            D{0}
            T{1}
            L{2}
            M{3}
            ^""".format(qif_date, qif_amount, qif_transfer, memo))

        actual_record, actual_file = self._converter.convert(
            date, debit, credit, amount, memo)

        self.assertEqual(expected_record, actual_record)
        self.assertEqual(expected_file, actual_file)

    # _format_qif_record() tests.
    def test__format_qif_record__expected_output(self):
        """
        Test for correct format of a QIF record.
        """
        date = ""
        amount = "-5.25"
        transfer = self._EXPENSES.values()[0]
        memo = "sample memo"
        expected = textwrap.dedent(
            """\
            D{0}
            T{1}
            L{2}
            M{3}
            ^""".format(date, amount, transfer, memo))
        actual = self._converter._format_qif_record(
            date, transfer, amount, memo)
        self.assertEqual(expected, actual)

    # _format_amount() tests.
    def test__format_amount__invalid_amount(self):
        """
        Test for an amount that cannot be converted to float.
        """
        debit = self._ASSETS.keys()[0]
        amount = "5.01a"
        expected_message = "amount ({0}) cannot be converted to float".format(amount)
        with self.assertRaises(ValueError) as context:
            self._converter._format_amount(debit, amount)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__format_amount__debit_is_expense(self):
        """
        Test for output amount when debit is an expense.
        """
        debit = self._EXPENSES.keys()[0]
        amount = "25.15"
        expected = "-25.15"
        actual = self._converter._format_amount(debit, amount)
        self.assertEqual(expected, actual)

    def test__format_amount__debit_is_not_expense(self):
        """
        Test for output amount when debit is not an expense.
        """
        debit = self._ASSETS.keys()[0]
        amount = "10.75"
        expected = "10.75"
        actual = self._converter._format_amount(debit, amount)
        self.assertEqual(expected, actual)

    def test__format_amount__invalid_debit_account(self):
        """
        Test for a debit account that is invalid and does not exist.
        """
        debit = "non-existant account"
        amount = "10.00"
        expected_message = "account key ({0}) does not exist".format(debit)
        with self.assertRaises(KeyError) as context:
            self._converter._format_amount(debit, amount)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__format_amount__output_is_two_decimal_places(self):
        """
        Test various inputs that output is two decimal places.
        """
        debit = self._ASSETS.keys()[0]

        amount = "5"
        expected = "5.00"
        actual = self._converter._format_amount(debit, amount)
        self.assertEqual(expected, actual)

        amount = "10.2"
        expected = "10.20"
        actual = self._converter._format_amount(debit, amount)
        self.assertEqual(expected, actual)

        amount = "20.45"
        expected = "20.45"
        actual = self._converter._format_amount(debit, amount)
        self.assertEqual(expected, actual)

        amount = "100.4550"
        expected = "100.45"
        actual = self._converter._format_amount(debit, amount)
        self.assertEqual(expected, actual)

        amount = "100.4551"
        expected = "100.46"
        actual = self._converter._format_amount(debit, amount)
        self.assertEqual(expected, actual)

    # _format_date() tests.
    def test__format_date__current_date(self):
        """
        Test the expected output using the current date.
        """
        date = time.localtime()
        expected = time.strftime("%m/%d/%Y", date)
        actual = self._converter._format_date(date)
        self.assertEqual(expected, actual)

    def test__format_date__overflow_error(self):
        """
        Test for a date that cannot be converted to C long.
        """
        date = (9999999999,0,0,0,0,0,0,0,0)
        expected_message = (
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because Python int too large to convert to C long")
        with self.assertRaises(OverflowError) as context:
            self._converter._format_date(date)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__format_date__past_date(self):
        """
        Test the expected output using a past date.
        """
        date = time.gmtime(0)
        expected = "01/01/1970"
        actual = self._converter._format_date(date)
        self.assertEqual(expected, actual)

    def test__format_date__type_error(self):
        """
        Test for a date that is invalid.
        """
        date = "invalid date type"
        expected_message = (
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because argument must be 9-item sequence, not str")
        with self.assertRaises(TypeError) as context:
            self._converter._format_date(date)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__format_date__value_error(self):
        """
        Test for a date that is out of range.
        """
        date = (1000,0,0,0,0,0,0,0,0)
        expected = (
            "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
            "because year out of range")
        with self.assertRaises(ValueError) as context:
            self._converter._format_date(date)
        actual = context.exception.message
        self.assertEqual(expected, actual)

    # _get_qif_file() tests.
    def test__get_qif_file__both_have_file(self):
        """
        Test for a valid debit key (that has an associated file) and a valid
        credit key (that has an associated file). Expect back the file
        associated with the debit key since it has higher priority.
        """
        debit = self._FILES.keys()[0]
        credit = self._FILES.keys()[1]
        expected = self._FILES[debit]
        actual = self._converter._get_qif_file(debit, credit)
        self.assertEqual(expected, actual)

    def test__get_qif_file__both_have_no_file(self):
        """
        Test for a invalid debit key (that has no associated file) and an
        invalid credit key (that has no associated file).
        """
        debit = self._ACCOUNTS_WITHOUT_FILE.keys()[0]
        credit = self._ACCOUNTS_WITHOUT_FILE.keys()[1]
        expected_message = (
            "neither debit key ({0}) ".format(debit) +
            "or credit key ({0}) ".format(credit) +
            "has an associated QIF file")
        with self.assertRaises(KeyError) as context:
            self._converter._get_qif_file(debit, credit)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__get_qif_file__debit_has_file_and_credit_has_no_file(self):
        """
        Test for a valid debit key (that has an associated file) and an
        invalid credit key (that has no associated file).
        """
        debit = self._FILES.keys()[0]
        credit = self._ACCOUNTS_WITHOUT_FILE.keys()[0]
        expected = self._FILES[debit]
        actual = self._converter._get_qif_file(debit, credit)
        self.assertEqual(expected, actual)

    def test__get_qif_file__debit_has_no_file_and_credit_has_file(self):
        """
        Test for a invalid debit key (that has no associated file) and a
        valid credit (that has an associated file).
        """
        debit = self._ACCOUNTS_WITHOUT_FILE.keys()[0]
        credit = self._FILES.keys()[0]
        expected = self._FILES[credit]
        actual = self._converter._get_qif_file(debit, credit)
        self.assertEqual(expected, actual)

    # _get_transfer_account() tests.
    def test__get_transfer_account__both_have_file(self):
        """
        Test for debit and credit keys that both have have associated QIF
        files and associated QIF accounts. Expect back the account
        associated with the credit key since it has lower priority.
        """
        debit = self._FILES.keys()[0]
        credit = self._FILES.keys()[1]
        expected = self._ACCOUNTS[credit]
        actual = self._converter._get_transfer_account(debit, credit)
        self.assertEqual(expected, actual)

    def test__get_transfer_account__both_have_no_file(self):
        """
        Test for a invalid debit key (that has no associated file) and an
        invalid credit key (that has no associated file).
        """
        debit = self._ACCOUNTS_WITHOUT_FILE.keys()[0]
        credit = self._ACCOUNTS_WITHOUT_FILE.keys()[1]
        expected_message = (
            "neither debit key ({0}) ".format(debit) +
            "or credit key ({0}) ".format(credit) +
            "has an associated QIF file")
        with self.assertRaises(KeyError) as context:
            self._converter._get_transfer_account(debit, credit)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    def test__get_transfer_account__debit_has_file_and_credit_has_no_file(self):
        """
        Test for a valid debit key (that has an associated file) and a
        valid credit key (that has no associated file).
        """
        debit = self._FILES.keys()[0]
        credit = self._ACCOUNTS_WITHOUT_FILE.keys()[0]
        expected = self._ACCOUNTS[credit]
        actual = self._converter._get_transfer_account(debit, credit)
        self.assertEqual(expected, actual)

    def test__get_transfer_account__debit_has_no_file_and_credit_has_file(self):
        """
        Test for a valid debit key (that has no associated file) and a
        valid credit (that has an associated file).
        """
        debit = self._ACCOUNTS_WITHOUT_FILE.keys()[0]
        credit = self._FILES.keys()[1]
        expected = self._ACCOUNTS[debit]
        actual = self._converter._get_transfer_account(debit, credit)
        self.assertEqual(expected, actual)

    def test__get_transfer_account__account_key_not_in_accounts(self):
        """
        Test for accounts with associated QIF files but with no
        associated account.
        """
        debit = "invalid account key"
        credit = self._FILES.keys()[0]
        expected_message = (
            "account key ({0}) ".format(debit) +
            "does not have has an associated QIF account")
        with self.assertRaises(KeyError) as context:
            self._converter._get_transfer_account(debit, credit)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

    # _get_transfer_account() with _get_qif_file() tests.
    def test__get_transfer_account_and_get_qif_file_return_unique(self):
        """
        Test to ensure that if get_transfer_account returned the debit acount
        then get_qif_file returned the credit file and vice versa.
        """
        debit = self._FILES.keys()[0]
        credit = self._FILES.keys()[1]

        expected_file = self._FILES[debit]
        actual_file = self._converter._get_qif_file(debit, credit)
        self.assertEqual(expected_file, actual_file)

        expected_account = self._ACCOUNTS[credit]
        actual_account = self._converter._get_transfer_account(debit, credit)
        self.assertEqual(expected_account, actual_account)

    # __init__()
    def test__init__key_in_files_is_not_in_accounts(self):
        """
        Test to ensure that all keys in files must exist in accounts.
        """
        extra_key = "filekey"
        extra_file = filesystem.MockFile("./", "filekey.qif")
        files = dict(
            self._FILES.items() +
            [(extra_key, extra_file)])
        expected_message = (
            "account key ({0}) ".format(extra_key) +
            "for file ({0}) ".format(extra_file.filename) +
            "does not have has an associated QIF account")
        with self.assertRaises(ValueError) as context:
            transactionconverter.QifConverter(
                self._log, files, self._ACCOUNT_TYPES, self._ASSETS,
                self._LIABILITIES, self._REVENUES, self._EXPENSES)
        actual_message = context.exception.message
        self.assertEqual(expected_message, actual_message)

if __name__ == '__main__':
    unittest.main(verbosity=2)
