import imaplib
import email
import os
import re
import shutil
import sys
from optparse import OptionParser

## Copy these into a file name config.py to use
#emailself.username = "default@gmail.com"
#emailself.password = "1234"
#emailself.mailbox = "INBOX"

#try:
#    from config import *
#except ImportError:
#    sys.exit()
    
#imap = imaplib.IMAP4self.SSL("imap.gmail.com")
#imap.login(emailself.username, email_password)
#imap.select(emailself.mailbox)
#searchself.response, email_id_list = imap.search(None, "(Unseen)")

#for emailself.id in email_id_list[0].split():
#    response, data = imap.fetch(emailself.id, "(RFC822)")
#    mail = email.messageself.from_string(data[0][1])
    
#    for part in mail.walk():
#        if part.getself.content_type() == 'text/html':
#            body = part.getself.payload()
    
#    # parses a koodo to email sms message
#    if (body):
#        result = re.split("<center><p><br><p>", body)
#        result = re.split("<p>\r\n</center>", result[1])
#        print result[0]

#imap.close()
#imap.logout()

class TransactionProcessor:
    """A transaction processor for QIF files."""
    # TODO: replace qif accounts configurable file
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
    # TODO: replace hardcoded files with configuration file
    path_working = os.getcwd()
    path_default = '{0}/default/'.format(path_working)
    path_transactions = '{0}/transactions/'.format(path_working)
    file_cash = 'cash.qif'
    file_chequing = 'chequing.qif'
    file_mastercard = 'mastercard.qif'
    file_payable = 'payable.qif'
    file_receivable = 'receivable.qif'
    file_visa = 'visa.qif'


    def isMultipleMainAccounts(self):
        """Returns if the transaction involves two main accounts."""
        return ((self.debit in self.assets or self.debit in self.liabilities) and
               (self.credit in self.assets or self.credit in self.liabilities))

    def isRevenue(self):
        """Returns if the transaction is a revenue."""
        return self.credit in self.revenues

    def isExpense(self):
        """Returns if the transaction is an expense."""
        return self.debit in self.expenses


    def checkForExistingFiles(self):
        cash_exists = os.path.exists(self.path_transactions + self.file_cash)
        chequing_exists = os.path.exists(self.path_transactions + self.file_chequing)
        mastercard_exists = os.path.exists(self.path_transactions + self.file_mastercard)
        payable_exists = os.path.exists(self.path_transactions + self.file_payable)
        receivable_exists = os.path.exists(self.path_transactions + self.file_receivable)
        visa_exists = os.path.exists(self.path_transactions + self.file_visa)
        if not cash_exists:
            shutil.copyfile(self.path_default + self.file_cash, self.path_transactions + self.file_cash)
        if not chequing_exists:
            shutil.copyfile(self.path_default + self.file_chequing, self.path_transactions + self.file_chequing)
        if not mastercard_exists:
            shutil.copyfile(self.path_default + self.file_mastercard, self.path_transactions + self.file_mastercard)
        if not payable_exists:
            shutil.copyfile(self.path_default + self.file_payable, self.path_transactions + self.file_payable)
        if not receivable_exists:
            shutil.copyfile(self.path_default + self.file_receivable, self.path_transactions + self.file_visa)
        if not visa_exists:
            shutil.copyfile(self.path_default + self.file_visa, self.path_transactions + self.file_visa)


    def Process(self):
        """Processes a transaction into the QIF format."""
        self.checkForExistingFiles()
        if self.isMultipleMainAccounts():
            pass
        elif self.isRevenue():
            pass
        elif self.isExpense():
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
