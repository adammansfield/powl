import ConfigParser
import imaplib
import email
import logging
import os
import re
import shutil
import sys
import time
import optparse
from transaction import TransactionProcessor
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%H:%M')

class Powl:
    path_default = os.getcwd() + os.sep + 'default'
    path_logs = os.getcwd() + os.sep + 'logs'
    path_transactions = os.getcwd() + os.sep + 'transactions'

    def read_inbox(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('config.cfg'))
        address = config.get('Email','address')
        password = config.get('Email','password')
        logging.debug('%s %s', address, password)
        pass
        
    def parse_message(self, message):
        """Parses a message and does a corresponding action."""
        # TODO: parse date from email
        date = "2012-03-26 10:23:12"
        date = time.strptime(date, "%Y-%m-%d %H:%M:%S")

        options = re.split(' -', message)
        if options[0] == 'transaction':
            self.parse_transaction(options, date)

    def parse_transaction(self, options, date):
        for option in options:
            if re.match('d', option):
                debit = option.replace('d ','')
            elif re.match('c', option):
                credit = option.replace('c ','')
            elif re.match('a', option):
                amount = option.replace('a ','')
            elif re.match('m', option):
                memo = option.replace('m ','')
                memo = memo.replace("\"", '')
        self.transaction.Process(date,
                                 debit,
                                 credit,
                                 amount,
                                 memo)
            
    def main(self):
        self.read_inbox()
        #self.transaction = TransactionProcessor(self.path_default,
        #                                        self.path_transactions,
        #                                        self.path_logs)
        #message = "transaction -d din -c m -a 5.65 -m \"lunch at subway\""
        #self.parse_message(message)
    
if __name__ == '__main__':
    Powl().main()
