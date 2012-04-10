#!/usr/bin/env python
"""Processing transaction data into the QIF format."""
# Builtin
import os
import shutil
import time
# Powl
import logger

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

    # File IO
    # -------
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

    # Transaction Processing
    # ----------------------
    def Process(self, date, debit, credit, amount, memo):
        """Process a transaction into the QIF format."""
        valid_accounts = (debit in self.accounts and
                          credit in self.accounts)
        valid_files = (debit in self.filenames or
                       credit in self.filenames)
        if valid_accounts and valid_files:
            filename, transaction = self.format_to_qif(date,
                                                       debit,
                                                       credit,
                                                       amount,
                                                       memo)
            self.check_for_existing_files()
            self.append_transaction_to_file(filename, transaction)
        else:
            self.notify_transaction_error()
            self.log_transaction_error(date, debit, credit, amount, memo)
            
    def format_to_qif(self, date, debit, credit, amount, memo):
        """Formats transaction data into the QIF format for a specific file."""
        if debit in self.filenames:
            filename = self.filenames.get(debit)
            transfer = self.accounts.get(credit)
        else:
            filename = self.filenames.get(credit)
            transfer = self.accounts.get(debit)
        if debit in self.expenses:
            amount = -float(amount)
        date = time.strftime('%m/%d/%Y', date)
        transaction = ("D{0}{1}".format(date, os.linesep) + 
                       "T{0}{1}".format(amount, os.linesep) +
                       "L{0}{1}".format(transfer, os.linesep) +
                       "M{0}{1}".format(memo, os.linesep) +
                       "^{0}".format(os.linesep))
        self.log_transaction(date, filename, transfer, amount, memo)
        return filename, transaction

    def notify_transaction_error(self):
        # TODO: send email detailing the error
        pass

    # Logging
    # -------
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
        logger.info(logmsg)

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
        logger.error(logmsg)

    # Initialization
    # --------------
    def __init__(self, default_path, transaction_path, log_path):
        """Set the paths used for transaction files."""
        self.default_path = default_path
        self.log_path = log_path
        self.transaction_path = transaction_path
