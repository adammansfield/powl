import imaplib
import email
import re
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
    ASSETS = {
        "c": "Assets:Current:Cash",
        "n": "Assets:Current:Chequing",
        "r": "Assets:Current:Receivable",
        "s": "Assets:Current:Savings",
    }
    LIABILITIES = {
        "m": "Liabilities:Mastercard",
        "p": "Liabilities:Payable",
        "v": "Liabilities:Visa",
    }
    REVENUES = {
        "ear": "Income:Earnings",
        "gif": "Income:Gifts",
        "int": "Income:Interest",
        "mis": "Income:Miscellaneous",
        "por": "Income:Portfolio",
    }
    EXPENSES = {
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

    def isMultipleMainAccounts(self):
        """Returns if the transaction involves two main accounts."""
        return ((self.debit in self.ASSETS or self.debit in self.LIABILITIES) and
               (self.credit in self.ASSETS or self.credit in self.LIABILITIES))

    def isRevenue(self):
        """Returns if the transaction is a revenue."""
        return self.credit in self.REVENUES

    def isExpense(self):
        """Returns if the transaction is an expense."""
        return self.debit in self.EXPENSES

    def Process(self):
        """Processes a transaction into the QIF format."""
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
