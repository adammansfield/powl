import imaplib
import email
import os
import re
import shutil
import sys
import time
from optparse import OptionParser

path_default = os.getcwd() + os.path.sep + 'default'
path_logs = os.getcwd() + os.path.sep + 'logs'
path_transactions = os.getcwd() + os.path.sep + 'transactions'

class TransactionProcessor:
    """A transaction processor for QIF files."""
    # TODO: replace qif accounts and files with a configurable file
    filenames = {
        "c": "cash.qif",
        "n": "chequing.qif",
        "m": "mastercard.qif",
        "p": "payable.qif",
        "r": "receivable.qif",
        "v": "visa.qif",
    }
    accounts = {
        "c": "Assets:Current:Cash",
        "n": "Assets:Current:Chequing",
        "r": "Assets:Current:Receivable",
        "s": "Assets:Current:Savings",
        "m": "Liabilities:Mastercard",
        "p": "Liabilities:Payable",
        "v": "Liabilities:Visa",
        "ear": "Revenue:Earnings",
        "gif": "Revenue:Gifts",
        "int": "Revenue:Interest",
        "mis": "Revenue:Miscellaneous",
        "por": "Revenue:Portfolio",
        "gas": "Expenses:Auto:Gas",
        "ins": "Expenses:Auto:Insurance",
        "mai": "Expenses:Auto:Maintenance & Fees",
        "clo": "Expenses:Commodities:Clothing",
        "com": "Expenses:Commodities:Computer",
        "woe": "Expenses:Commodities:Workout Equipment",
        "din": "Expenses:Entertainment:Dining",
        "gam": "Expenses:Entertainment:Games",
        "ent": "Expenses:Entertainment:General",
        "out": "Expenses:Entertainment:Outtings",
        "mis": "Expenses:Miscellanous:General",
        "gif": "Expenses:Miscellanous:Gifts",
        "los": "Expenses:Miscellanous:Loss",
        "eye": "Expenses:Upkeep:Eyewear",
        "nut": "Expenses:Upkeep:Nutrition",
        "sup": "Expenses:Upkeep:Supplies",
        "pho": "Expenses:Utilities:Phone",
    }

    def checkForExistingFiles(self):
        """Copies default QIF files if custom files are missing."""
        for filename in self.filenames.itervalues():
            custom_file = path_transactions + os.path.sep + filename
            if not os.path.isfile(custom_file):
                default_file = path_default + os.path.sep + filename
                shutil.copyfile(default_file, custom_file)

    def Process(self):
        """Processes a transaction into the QIF format."""
        self.checkForExistingFiles()
        if self.debit in self.filenames:
            file = self.files.get(self.debit)
        elif self.credit in self.filenames:
            file = self.files.get(self.credit)
        else:
            file_log = path_logs + '/' + time.strftime('%Y-%m-%d', time.localtime()) + '.log'
            log = open(file_log, 'a')
            log_time = time.strftime('[%H:%M]', time.localtime())
            log_debit = 'Debit: ' + self.debit
            log_credit = 'Credit: ' + self.credit
            log_amount = 'Amount: ' + self.amount
            log_memo = 'Memo: ' + self.memo
            message = '{0} {1} {2} {3} {4} {5}'.format(log_time, log_debit, log_credit, log_amount, log_memo, os.linesep)
            log.write(message)
            log.close()
        self.amount = 'T-{0}'.format(self.amount)
        data = '{0}'.format(self.amount)

    def __init__(self, date, debit, credit, amount, memo):
        """Sets the transaction data."""
        self.date = date
        self.debit = debit
        self.credit = credit
        self.amount = amount
        self.memo = memo

def main():
    parser = OptionParser()
    parser.add_option("--transaction")
    parser.add_option("-d", type="string", dest="debit", default="")
    parser.add_option("-c", type="string", dest="credit", default="")
    parser.add_option("-a", type="string", dest="amount", default="")
    parser.add_option("-m", type="string", dest="memo", default="")
    (options, args) = parser.parse_args()
    # TODO: parse date from email
    date = "2012-03-26"
    transaction = TransactionProcessor(date,
                                       options.debit,
                                       options.credit,
                                       options.amount,
                                       options.memo)
    transaction.Process()
    
if __name__ == '__main__':
    main()
