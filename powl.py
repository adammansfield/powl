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
import TransactionProcessor
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%H:%M')

class Powl:
    """Class for processing emails to do a corresponding action."""

    # Email Processing
    # ----------------
    def process_inbox(self):
        """Processes a list of messages to pass onto parsing."""
        search_response, email_ids = self.imap.search(None, "(Unseen)")
        for email_id in email_ids[0].split():
            fetch_response, data = self.imap.fetch(email_id, "(RFC822)")
            mail = email.message_from_string(data[0][1])
            date = email.utils.parsedate(mail['Date'])
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload()
                    message = self.strip_message_markup(body)
                    logging.debug('EMAIL: %s - %s', message, date)
                    self.parse_message(message, date)

    def strip_message_markup(self, message):
        """Returns email message striped of markup."""
        retval = message
        retval = retval.replace('<P>','')
        retval = retval.replace('</P>','')
        retval = retval.replace('=0A',' ')
        return retval

    # Parsing
    # -------
    def parse_message(self, message, date):
        """Parses a message and does a corresponding action."""
        # TODO: parse date from email
        params = re.split(' -', message)
        if params[0].strip() == 'transaction':
            self.parse_transaction(params, date)
        else:
            # TODO: append to miscellaneous file
            logging.debug('No match: %s', message)

    def parse_transaction(self, params, date):
        """Separates transaction data and processes the transaction."""
        for param in params:
            if re.match('d', param):
                debit = param.replace('d ','')
            elif re.match('c', param):
                credit = param.replace('c ','')
            elif re.match('a', param):
                amount = param.replace('a ','')
            elif re.match('m', param):
                memo = param.replace('m ','')
                memo = memo.replace("\"", '')
        log = 'Debit: %s Credit: %s Amount: %s Memo: %s'
        logging.debug(log, debit, credit, amount, memo)
        self.transaction.Process(date, debit, credit, amount, memo)
    

    # Initialization
    # --------------
    def main(self):
        self.load_config()
        self.initialize_modules()
        self.process_inbox()

    def load_config(self):
        """Reads custom config file and loads settings."""
        config = ConfigParser.ConfigParser()
        config.readfp(open('config.cfg'))
        self.address = config.get('Email','address')
        self.password = config.get('Email','password')
        self.mailbox = config.get('Email', 'mailbox')
        workingdir = os.getcwd() + os.sep
        self.path_default = workingdir + config.get('Paths', 'default')
        self.path_logs = workingdir + config.get('Paths', 'logs')
        self.path_transactions = workingdir + config.get('Paths', 'transactions')
        logging.debug('%s %s %s', self.address, self.password, self.mailbox)

    def initialize_modules(self):
        """Intializes modules used for doing various actions."""
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(self.address, self.password)
        self.imap.select(self.mailbox)
        self.transaction = TransactionProcessor.TransactionProcessor(self.path_default,
                                                                     self.path_transactions,
                                                                     self.path_logs)
    
if __name__ == '__main__':
    Powl().main()
