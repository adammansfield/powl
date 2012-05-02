#!/usr/bin/env python
"""Process transaction data into the QIF format."""
import logging
import os
import shutil
import time
from powl.logger import logger

class TransactionProcessor:
    """A transaction processor for QIF files."""
    # TODO: replace qif accounts and files with a configurable file
    filenames = {
        'c': "cash.qif",
        'n': "chequing.qif",
        'm': "mastercard.qif",
        'p': "payable.qif",
        'r': "receivable.qif",
        'v': "visa.qif",
    }
    assets = {
        'c': "Assets:Current:Cash",
        'n': "Assets:Current:Chequing",
        'r': "Assets:Current:Receivable",
        's': "Assets:Current:Savings",
    }
    liabilities = {
        'm': "Liabilities:Mastercard",
        'p': "Liabilities:Payable",
        'v': "Liabilities:Visa",
    }
    revenues = { 
        'ear': "Revenue:Earnings",
        'gif': "Revenue:Gifts",
        'int': "Revenue:Interest",
        'mis': "Revenue:Miscellaneous",
        'por': "Revenue:Portfolio",
    }
    expenses = {
        'gas': "Expenses:Auto:Gas",
        'ins': "Expenses:Auto:Insurance",
        'mai': "Expenses:Auto:Maintenance & Fees",
        'clo': "Expenses:Commodities:Clothing",
        'com': "Expenses:Commodities:Computer",
        'woe': "Expenses:Commodities:Workout Equipment",
        'din': "Expenses:Entertainment:Dining",
        'gam': "Expenses:Entertainment:Games",
        'ent': "Expenses:Entertainment:General",
        'out': "Expenses:Entertainment:Outtings",
        'mis': "Expenses:Miscellanous:General",
        'gif': "Expenses:Miscellanous:Gifts",
        'los': "Expenses:Miscellanous:Loss",
        'eye': "Expenses:Upkeep:Eyewear",
        'nut': "Expenses:Upkeep:Nutrition",
        'sup': "Expenses:Upkeep:Supplies",
        'pho': "Expenses:Utilities:Phone",
    }
    accounts = dict(assets.items() +
                    liabilities.items() +
                    revenues.items() +
                    expenses.items())

    # FILE IO
    def check_for_existing_files(self):
        """Copies default QIF files if custom files are missing."""
        for filename in self.filenames.itervalues():
            custom_file = self.transaction_path + os.sep + filename
            if not os.path.isfile(custom_file):
                default_file = self.default_path + os.sep + filename
                if os.path.isfile(default_file):
                    shutil.copyfile(default_file, custom_file)

    def append_transaction_to_file(self, filename, transaction):
        """Append a formatted transaction to the specified file."""
        filename = self.transaction_path + os.sep + filename 
        file = open(filename, 'a')
        file.write(transaction)
        file.close()

    # TRANSACTION PROCESSING
    def Process(self, date, debit, credit, amount, memo):
        """Process a transaction into the QIF format and write to file."""
        if self.valid_transaction(date, debit, credit, amount):
            qif_date = self.qif_convert_date(date)
            qif_filename = self.qif_convert_filename(debit, credit)
            qif_transfer = self.qif_convert_transfer(debit, credit)
            qif_amount = self.qif_convert_amount(debit, amount)
            qif_memo = memo
            qif_transaction = self.qif_format(qif_date,
                                              qif_transfer,
                                              qif_amount,
                                              qif_memo)
            self.check_for_existing_files()
            self.append_transaction_to_file(qif_filename, qif_transaction)
            self.log_transaction(qif_date,
                                 qif_filename,
                                 qif_transfer,
                                 qif_amount,
                                 qif_memo)
        else:
            # TODO: return an error for powl.py to handle
            self.log_transaction_error(date, debit, credit, amount, memo)

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
    def qif_format(self, date, transfer, amount, memo):
        """Formats qif data into a transaction for a QIF file."""
        fmt_date = 'D' + date
        fmt_amount = 'T' + amount
        fmt_transfer = 'L' + transfer
        fmt_memo = 'M' + memo
        fmt_sep = '^'
        fmt_transaction = (fmt_date + os.linesep + 
                           fmt_amount + os.linesep + 
                           fmt_transfer + os.linesep + 
                           fmt_memo + os.linesep + 
                           fmt_sep + os.linesep)
        return fmt_transaction

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
        file = os.path.basename(path)
        logindent = '\t\t\t\t  '
        logmsg = ("TRANSACTION{0}".format(os.linesep) +
                  "{0}date: {1}{2}".format(logindent, date, os.linesep) +
                  "{0}file: {1}{2}".format(logindent, file, os.linesep) +
                  "{0}transfer: {1}{2}".format(logindent, transfer, os.linesep) +
                  "{0}amount: {1}{2}".format(logindent, amount, os.linesep) +
                  "{0}memo: {1}{2}".format(logindent, memo, os.linesep))
        self.log.info(logmsg)

    def log_transaction_error(self, date, debit, credit, amount, memo):
        """Logs the transaction."""
        date = time.strftime('%m/%d/%Y', date)
        logindent = '\t\t\t\t  '
        logmsg = ("TRANSACTION{0}".format(os.linesep) +
                  "{0}date: {1}{2}".format(logindent, date, os.linesep) +
                  "{0}debit: {1}{2}".format(logindent, debit, os.linesep) +
                  "{0}credit: {1}{2}".format(logindent, credit, os.linesep) +
                  "{0}amount: {1}{2}".format(logindent, amount, os.linesep) +
                  "{0}memo: {1}{2}".format(logindent, memo, os.linesep))
        self.log.error(logmsg)

    # INITIALIZATION
    def __init__(self, default_path="", transaction_path="", log_path=""):
        """Set the paths used for transaction files."""
        self.default_path = default_path
        self.log_path = log_path
        self.transaction_path = transaction_path
        if log_path != "":
            self.log = logger.Logger("TransactionProcessor", self.log_path)
