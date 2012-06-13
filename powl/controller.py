#!/usr/bin/env python
"""Initialize, start and handle module interaction."""
import ConfigParser
import email
import imaplib
import logging
import optparse
import os
import re
import shutil
import sys
import textwrap
import time
import powl.logger as logger
import powl.output as output
from powl.config import Config
from powl.transaction import Transaction

class Controller:

    # Email Processing
    def start(self):
        """Parse through an inbox of emails."""
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(self.config.address, self.config.password)
        self.imap.select(self.config.mailbox)
        search_response, email_ids = self.imap.search(None, "(Unseen)")
        logger.info("PROCESSING INBOX")
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
        retval = retval.replace('&amp;','&')
        return retval

    def parse_message(self, message, date):
        """Parse a message and determine its specified action."""
        # TODO: parse date from email
        action, data = message.split(' ',1)
        if action == 'transaction':
            self.process_transaction(data, date)
        elif action == 'todo':
            self.process_todo(data, date)
        else:
            self.process_miscellaneous(data, date)

    # Action Processing
    def process_miscellaneous(self, data, date):
        """Write miscellaneous message to file."""
        filename = os.path.join(self.config.output_dir, 'miscellaneous.txt')
        file = open(filename, 'a')
        file.write(data)
        file.close()
        logger.info('MISC\t%s', data)

    def process_todo(self, task, date):
        """Send task to toodledo."""
        pass
        
    def process_transaction(self, params, date):
        """Separate transaction data to pass onto processing."""
        #debit, credit, amount, memo = self.message.transaction(params)
        #filename, data = self.transaction.process(date, debit, credit, amount, memo)
        #output.append(filename, data)
        params = re.split(' -', params)
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
                memo = memo.strip()
        self.transaction.process(date, debit, credit, amount, memo)

    




    # FILE I/O
    def _create_directories(self):
        """Create the configured directories if they do not exist."""
        output.makedir(self.config.directories)

    def _create_transaction_templates(self):
        """Create transaction templates if files do not exist."""
        templates = self.transaction.get_templates()
        for filename, template in templates:
            filepath = os.path.join(self.config.transaction_dir, filename)
            if not os.path.isfile(filepath):
                output.write(filepath, template)
         
    # LOADING
    def _load_config(self):
        """Load the configuration settings."""
        self.config = Config()
        if not os.path.isfile(self.config.config_filepath):
            output.write(self.config.config_filepath,
                         self.config_file_layout)
        self.config.read()

    def _load_processors(self):
        """Load the processors with custom config settings."""
        self.transaction = Transaction(self.config.qif_filenames,
                                       self.config.qif_types,
                                       self.config.qif_assets,
                                       self.config.qif_liabilities,
                                       self.config.qif_revenues,
                                       self.config.qif_expenses)

    # INITIALIZATION
    def __init__(self):
        """Setup and process email inbox."""
        logger.initialize(logger.FORMAT_WEEKLY)
        self._load_config()
        self._create_directories()
        logger.set_file_handler(self.config.log_dir)
        self._load_processors()
        self._create_transaction_templates()

