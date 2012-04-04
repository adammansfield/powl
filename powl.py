import imaplib
import email
import os
import re
import shutil
import sys
import time
import transaction
import optparse

class Paths:
    default = os.getcwd() + os.path.sep + 'default'
    logs = os.getcwd() + os.path.sep + 'logs'
    transactions = os.getcwd() + os.path.sep + 'transactions'

def main():
    # TODO: replace OptionParser with string parsing
    parser = optparse.OptionParser()
    parser.add_option("--transaction")
    parser.add_option("-d", type="string", dest="debit", default="")
    parser.add_option("-c", type="string", dest="credit", default="")
    parser.add_option("-a", type="string", dest="amount", default="")
    parser.add_option("-m", type="string", dest="memo", default="")
    (options, args) = parser.parse_args()
    # TODO: parse date from email
    date = "2012-03-26 10:23:12"
    date = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    accounting = transaction.Transaction(date,
                                         options.debit,
                                         options.credit,
                                         options.amount,
                                         options.memo)
    accounting.Process()
    
if __name__ == '__main__':
    main()
