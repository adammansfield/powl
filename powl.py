#!/usr/bin/env python
"""Process an email inbox to do a correpsonding action with each message."""
# Builtin
import ConfigParser
import imaplib
import email
import os
import re
import shutil
import sys
import time
import optparse
# Powl
import logger
import TransactionProcessor
__version__ = "0.1.01"

class Powl:
    """Class for processing emails to do a corresponding action."""
    # Email Processing
    # ----------------
    def process_inbox(self):
        """Process a list of messages to be parsed."""
        logger.info("PROCESSING INBOX")
        search_response, email_ids = self.imap.search(None, "(Unseen)")
        for email_id in email_ids[0].split():
            fetch_response, data = self.imap.fetch(email_id, "(RFC822)")
            mail = email.message_from_string(data[0][1])
            date = email.utils.parsedate(mail['Date'])
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload()
                    message = self.strip_message_markup(body)
                    logger.debug('EMAIL   %s', message.strip())
                    self.parse_message(message, date)

    def strip_message_markup(self, message):
        """Return message striped of markup."""
        retval = message
        retval = retval.replace('<P>','')
        retval = retval.replace('</P>','')
        retval = retval.replace('=0A',' ')
        return retval

    # Parsing
    # -------
    def parse_message(self, message, date):
        """Parse a message and determine its specified action."""
        # TODO: parse date from email
        params = re.split(' -', message)
        if params[0].strip() == 'transaction':
            self.parse_transaction(params, date)
        else:
            # TODO: append to miscellaneous file
            logger.debug('MISC    %s', message)

    def parse_transaction(self, params, date):
        """Separate transaction data to pass onto processing."""
        for param in params:
            param = param.strip()
            if re.match('d', param):
                debit = param.replace('d ','')
            elif re.match('c', param):
                credit = param.replace('c ','')
            elif re.match('a', param):
                amount = param.replace('a ','')
            elif re.match('m', param):
                memo = param.replace('m ','')
                memo = memo.replace("\"", '')
        self.transaction.Process(date, debit, credit, amount, memo)

    # Initialization
    # --------------
    def main(self):
        """Setup and process email inbox."""
        self.load_config()
        self.initialize_modules()
        self.process_inbox()

    def load_config(self):
        """Load custom config file settings."""
        config = ConfigParser.ConfigParser()
        config.readfp(open('config.cfg'))
        self.address = config.get('Email','address')
        self.password = config.get('Email','password')
        self.mailbox = config.get('Email', 'mailbox')
        workingdir = os.getcwd() + os.sep
        self.path_default = workingdir + config.get('Paths', 'default')
        self.path_logs = workingdir + config.get('Paths', 'logs')
        self.path_transactions = workingdir + config.get('Paths', 'transactions')

    def initialize_modules(self):
        """Intialize modules used for doing various actions."""
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(self.address, self.password)
        self.imap.select(self.mailbox)
        self.transaction = TransactionProcessor. \
                           TransactionProcessor(self.path_default,
                                                self.path_transactions,
                                                self.path_logs)
    
if __name__ == '__main__':
    Powl().main()
