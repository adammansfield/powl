import os
import shutil
import time
import powl

class Transaction:
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
        "ear": "Revenue:Earnings",
        "gif": "Revenue:Gifts",
        "int": "Revenue:Interest",
        "mis": "Revenue:Miscellaneous",
        "por": "Revenue:Portfolio",
    }
    expenses = {
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
            custom_file = powl.Paths.transactions + os.path.sep + filename
            if not os.path.isfile(custom_file):
                default_file = powl.Paths.default + os.path.sep + filename
                shutil.copyfile(default_file, custom_file)

    def logTransactionError(self):
        """Logs the transaction error."""
        logtime = time.strftime('[%H:%M]', time.localtime())
        logdate = time.strftime('%Y-%m-%d', time.localtime())  
        transactiondate = time.strftime("%m/%d/%Y", self.date)
        message = (logtime +
                   " Date: " + transactiondate +
                   " Debit: " + self.debit +
                   " Credit: " + self.credit +
                   " Amount: " + self.amount +
                   " Memo: " + self.memo + os.linesep)
        logfile = powl.Paths.logs + os.path.sep + logdate + '.log'
        log = open(logfile, 'a')
        log.write(message)
        log.close()

    def formatToQif(self):
        """Formats transaction data into the QIF format for a specific file."""
        accounts = dict(self.assets.items() +
                        self.liabilities.items() +
                        self.revenues.items() +
                        self.expenses.items())
        if self.debit in self.filenames:
            filename = self.filenames.get(self.debit)
            transfer = accounts.get(self.credit)
        else:
            filename = self.filenames.get(self.credit)
            transfer = accounts.get(self.debit)
        if self.debit in self.expenses:
            amount = self.amount * -1
        else:
            amount = self.amount
        date = time.strftime("%m/%d/%Y", self.date)
        transaction = ("D{0}{1}".format(date, os.linesep) + 
                       "T{0}{1}".format(amount, os.linesep) +
                       "L{0}{1}".format(transfer, os.linesep) +
                       "M{0}{1}".format(self.memo, os.linesep) +
                       "^{0}".format(os.linesep))
        return filename, transaction

    def Process(self):
        """Processes a transaction into the QIF format."""
        valid_transaction = self.debit in self.filenames or self.credit in self.filenames
        if valid_transaction:
            self.checkForExistingFiles()
            filename, transaction = self.formatToQif()
            filename = powl.Paths.transactions + os.path.sep + filename 
            file = open(filename, 'a')
            file.write(transaction)
            file.close()
            print filename
            print transaction
        else:
            self.logTransactionError()

    def __init__(self, date, debit, credit, amount, memo):
        """Sets the transaction data."""
        self.date = date
        self.debit = debit
        self.credit = credit
        self.amount = amount
        self.memo = memo
