#!/usr/bin/env python
"""Process transaction data into the QIF format."""
import logging
import os
import shutil
import textwrap
import time
from powl import logger

class Transaction:

    # TEMPLATES
    def get_templates(self):
        templates = []
        for key, filename in self.filenames.iteritems():
            account_name = self.accounts.get(key)
            account_type = self.types.get(key)
            header = self.qif_format_header(account_name, account_type)
            template = (filename, header)
            templates.append(template)
        return templates

    # TRANSACTION PROCESSING
    def process(self, date, debit, credit, amount, memo):
        """Process a transaction into the QIF format and write to file."""
        if self.valid_transaction(date, debit, credit, amount):
            qif_date = self.qif_convert_date(date)
            qif_filename = self.qif_convert_filename(debit, credit)
            qif_transfer = self.qif_convert_transfer(debit, credit)
            qif_amount = self.qif_convert_amount(debit, amount)
            qif_memo = memo
            qif_transaction = self.qif_format_transaction(qif_date,
                                                          qif_transfer,
                                                          qif_amount,
                                                          qif_memo)
            self.log_transaction(qif_date,
                                 qif_filename,
                                 qif_transfer,
                                 qif_amount,
                                 qif_memo)
            return qif_filename, qif_transaction
        else:
            # TODO: return an error for powl.py to handle
            self.log_transaction_error(date, debit, credit, amount, memo)
            return None, None

    # VALIDITY
    def valid_accounts(self, debit, credit):
        """Check if both accounts are valid."""
        if debit in self.accounts and credit in self.accounts:
            return True
        else:
            return False

    def valid_amount(self, amount):
        """Check if amount is valid."""
        try:
            float(amount)
            return True
        except ValueError:
            return False

    def valid_date(self, date):
        """Check if date is valid."""
        try:
            time.mktime(date)
            return True
        except (TypeError, OverflowError, ValueError):
            return False


    def valid_file(self, debit, credit):
        """Check if one of the accounts is a file for qif."""
        if debit in self.filenames or credit in self.filenames:
            return True
        else:
            return False

    def valid_transaction(self, date, debit, credit, amount):
        """Check if the transaction is valid for qif formatting."""
        valid_accounts = self.valid_accounts(debit, credit)
        valid_amount = self.valid_amount(amount)
        valid_date = self.valid_date(date)
        valid_file = self.valid_file(debit, credit)
        return valid_accounts and valid_amount and valid_date and valid_file

    # QIF FORMATTING
    def qif_format_transaction(self, date, transfer, amount, memo):
        """Formats qif data into a transaction for a QIF file."""
        data = { 'date': date,
                 'amount': amount,
                 'transfer': transfer,
                 'memo': memo }
        transaction = textwrap.dedent("""\
            D{date}
            T{amount}
            L{transfer}
            M{memo}
            ^""".format(**data))
        return transaction

    def qif_format_header(self, account_name, account_type):
        """Format an account name and type into a header for a QIF file."""
        data = { 'name': account_name, 'type': account_type }
        header = textwrap.dedent("""\
            !Account
            N{name}
            T{type}
            ^
            !Type:{type}""".format(**data))
        return header

    # QIF CONVERSION
    def qif_convert_amount(self, debit, amount):
        """Convert amount based on debit."""
        if debit in self.expenses:
            return '-' + amount
        else:
            return amount

    def qif_convert_date(self, date):
        """Convert struct_time to qif date format."""
        return time.strftime('%m/%d/%Y', date)

    def qif_convert_filename(self, debit, credit):
        """Convert filename based on debit and credit."""
        if debit in self.filenames:
            return self.filenames.get(debit)
        else:
            return self.filenames.get(credit)

    def qif_convert_transfer(self, debit, credit):
        """Convert transfer account based on debit and credit."""
        if debit in self.filenames:
            return self.accounts.get(credit)
        else:
            return self.accounts.get(debit)

    # LOGGING
    def log_transaction(self, date, path, transfer, amount, memo):
        """Logs the transaction."""
        filename = os.path.basename(path)
        logindent = '\t\t\t\t  '
        # TODO: use textwrap.dedent
        logmsg = ("TRANSACTION{0}".format(os.linesep) +
                  "{0}date: {1}{2}".format(logindent, date, os.linesep) +
                  "{0}file: {1}{2}".format(logindent, filename, os.linesep) +
                  "{0}transfer: {1}{2}".format(logindent, transfer, os.linesep) +
                  "{0}amount: {1}{2}".format(logindent, amount, os.linesep) +
                  "{0}memo: {1}{2}".format(logindent, memo, os.linesep))
        logger.info(logmsg)

    def log_transaction_error(self, date, debit, credit, amount, memo):
        """Logs the transaction."""
        date = time.strftime('%m/%d/%Y', date)
        logindent = '\t\t\t\t  '
        # TODO: use textwrap.dedent
        logmsg = ("TRANSACTION{0}".format(os.linesep) +
                  "{0}date: {1}{2}".format(logindent, date, os.linesep) +
                  "{0}debit: {1}{2}".format(logindent, debit, os.linesep) +
                  "{0}credit: {1}{2}".format(logindent, credit, os.linesep) +
                  "{0}amount: {1}{2}".format(logindent, amount, os.linesep) +
                  "{0}memo: {1}{2}".format(logindent, memo, os.linesep))
        logger.error(logmsg)

    # INITIALIZATION
    def __init__(self, filenames, types, assets, liabilities, revenues, expenses):
        """Set the paths used for transaction files."""
        self.filenames = filenames
        self.types = types
        self.assets = assets
        self.liabilities = liabilities
        self.revenues = revenues
        self.expenses = expenses
        self.accounts = dict(self.assets.items() +
                             self.liabilities.items() +
                             self.revenues.items() +
                             self.expenses.items())
