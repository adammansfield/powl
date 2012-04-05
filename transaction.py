import os
import shutil
import time

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

    def check_for_existing_files(self):
        """Copies default QIF files if custom files are missing."""
        for filename in self.filenames.itervalues():
            custom_file = self.transaction_path + os.path.sep + filename
            if not os.path.isfile(custom_file):
                default_file = self.default_path + os.path.sep + filename
                if os.path.isfile(default_file):
                    shutil.copyfile(default_file, custom_file)

    def log_error(self, date, debit, credit, amount, memo):
        """Logs the transaction error."""
        logtime = time.strftime('[%H:%M]', time.localtime())
        logdate = time.strftime('%Y-%m-%d', time.localtime())  
        transactiondate = time.strftime('%m/%d/%Y', date)
        message = (logtime +
                   " Date: " + transactiondate +
                   " Debit: " + debit +
                   " Credit: " + credit +
                   " Amount: " + amount +
                   " Memo: " + memo + os.linesep)
        logfile = powl.Paths.logs + os.path.sep + logdate + '.log'
        log = open(logfile, 'a')
        log.write(message)
        log.close()

    def format_to_qif(self, date, debit, credit, amount, memo):
        """Formats transaction data into the QIF format for a specific file."""
        accounts = dict(self.assets.items() +
                        self.liabilities.items() +
                        self.revenues.items() +
                        self.expenses.items())
        if debit in self.filenames:
            filename = self.filenames.get(debit)
            transfer = accounts.get(credit)
        else:
            filename = self.filenames.get(credit)
            transfer = accounts.get(debit)
        if debit in self.expenses:
            amount = amount * -1
        date = time.strftime('%m/%d/%Y', date)
        transaction = ("D{0}{1}".format(date, os.linesep) + 
                       "T{0}{1}".format(amount, os.linesep) +
                       "L{0}{1}".format(transfer, os.linesep) +
                       "M{0}{1}".format(memo, os.linesep) +
                       "^{0}".format(os.linesep))
        return filename, transaction

    def append_transaction_to_file(self, filename, transaction):
        filename = self.transaction_path + os.path.sep + filename 
        file = open(filename, 'a')
        file.write(transaction)
        file.close()

    def Process(self, date, debit, credit, amount, memo):
        """Processes a transaction into the QIF format."""
        valid_transaction = debit in self.filenames or credit in self.filenames
        if valid_transaction:
            filename, transaction = self.format_to_qif(date,
                                                       debit,
                                                       credit,
                                                       amount,
                                                       memo)
            self.check_for_existing_files()
            self.append_transaction_to_file(filename, transaction)
        else:
            self.log_error()

    def __init__(self, default_path, transaction_path, log_path):
        """Sets the paths for the transaction files."""
        self.default_path = default_path
        self.log_path = log_path
        self.transaction_path = transaction_path
