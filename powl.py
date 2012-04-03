import imaplib
import email
import os
import re
import shutil
import sys
from optparse import OptionParser

class TransactionProcessor:
    """A transaction processor for QIF files."""
    # TODO: replace qif accounts and files with a configurable file
    transaction_files = {
        "c": "cash.qif",
        "n": "chequing.qif",
        "m": "mastercard.qif",
        "p": "payable.qif",
        "r": "receivable.qif",
        "v": "visa.qif",
    }
    assets = {
        "c": "Assets:Current:Cash",
        "n": "Assets:Current:Chequing",
        "r": "Assets:Current:Receivable",
        "s": "Assets:Current:Savings",
    }
    liabilities = {
        "m": "Liabilities:Mastercard",
        "p": "Liabilities:Payable",
        "v": "Liabilities:Visa",
    }
    revenues = {
        "ear": "Income:Earnings",
        "gif": "Income:Gifts",
        "int": "Income:Interest",
        "mis": "Income:Miscellaneous",
        "por": "Income:Portfolio",
    }
    expenses = {
        "gas":  "Expenses:Auto:Gas",
        "ins":  "Expenses:Auto:Insurance",
        "amai": "Expenses:Auto:Maintenance & Fees",
        "clo":  "Expenses:Commodities:Clothing",
        "com":  "Expenses:Commodities:Computer",
        "woe":  "Expenses:Commodities:Workout Equipment",
        "din":  "Expenses:Entertainment:Dining",
        "gam":  "Expenses:Entertainment:Games",
        "ent":  "Expenses:Entertainment:General",
        "out":  "Expenses:Entertainment:Outtings",
        "mis":  "Expenses:Miscellanous:General",
        "gif":  "Expenses:Miscellanous:Gifts",
        "los":  "Expenses:Miscellanous:Loss",
        "eye":  "Expenses:Upkeep:Eyewear",
        "nut":  "Expenses:Upkeep:Nutrition",
        "sup":  "Expenses:Upkeep:Supplies",
        "pho":  "Expenses:Utilities:Phone",
    }
    path_default = '{0}/default/'.format(os.getcwd())
    path_transactions = '{0}/transactions/'.format(os.getcwd())


    def isMultipleAccounts(self):
        """Returns if the transaction involves two main accounts."""
        files = self.transaction_files.itervalues()
        return self.debit in files and self.credit in files

    def isAnAccount(self):
        """Returns if the transaction involves at least one main account."""
        files = self.transaction_files.itervalues()
        return self.debit in files or self.credit in files


    def isRevenue(self):
        """Returns if the transaction is a revenue."""
        return self.credit in self.revenues

    def isExpense(self):
        """Returns if the transaction is an expense."""
        return self.debit in self.expenses


    def checkForExistingFiles(self):
        """Copies default QIF files if missing."""
        files = self.transaction_files.itervalues()
        for file in files:
            custom_file = '{0}/{1}'.format(self.path_transactions, file)
            exists = os.path.exists(custom_file)
            if not exists:
                default_file = '{0}/{1}'.format(self.path_default, file)
                shutil.copyfile(default_file, custom_file)


    def Process(self):
        """Processes a transaction into the QIF format."""
        self.checkForExistingFiles()
        if self.isMultipleAccounts():
            pass
        elif self.isAnAccount():
            pass
        else:
            pass
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
