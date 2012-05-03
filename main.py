#!/usr/bin/env python
"""Process an email inbox to do a correpsonding action with each message."""
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
from powl.logger import logger
from powl.processors import transaction

class Powl:
    """Class for processing emails to do a corresponding action."""
    
    default_mailbox = 'inbox'
    output_dir = os.getcwd() + os.sep + 'output'
    file_config = 'config.cfg'

    # Email Processing
    def process_inbox(self):
        """Parse through an inbox of emails."""
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(self.address, self.password)
        self.imap.select(self.mailbox)
        search_response, email_ids = self.imap.search(None, "(Unseen)")
        self.log.info("PROCESSING INBOX")
        for email_id in email_ids[0].split():
            fetch_response, data = self.imap.fetch(email_id, "(RFC822)")
            mail = email.message_from_string(data[0][1])
            date = email.utils.parsedate(mail['Date'])
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload()
                    message = self.strip_message_markup(body)
                    self.log.debug('EMAIL   %s', message.strip())
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
        filename = self.path_miscellaneous + os.sep + 'miscellaneous.txt'
        file = open(filename, 'a')
        file.write(data)
        file.close()
        self.log.info('MISC\t%s', data)

    def process_todo(self, task, date):
        """Send task to toodledo."""
        pass
        
    def process_transaction(self, params, date):
        """Separate transaction data to pass onto processing."""
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
        self.transaction.Process(date, debit, credit, amount, memo)

    # CONFIGURATION
    def config_create_default(self):
        """Create a default config file."""
        default_config_data = textwrap.dedent("""\
            [Email]
            address=
            password=
            mailbox=
            
            [Paths]
            output=output

            [Qif_Filenames]

            [Qif_Types]

            [Qif_Assets]

            [Qif_Liabilities]

            [Qif_Revenues] 

            [Qif_Expenses]""")
        file = open(self.file_config, 'a')
        file.write(default_config_data)
        file.close()

    def config_is_valid(self):
        """Check if the config is valid."""
        config = ConfigParser.ConfigParser()
        config.readfp(open(self.file_config))
        email_account = config.get('Email', 'address')
        if not email_account:
            self.log.info('Config file is not valid. Please enter your information.')
            return False
        else:
            return True

    def config_load(self):
        """Load custom config file settings."""
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open('config.cfg'))
        self.config_load_email()
        self.config_load_qif()
        self.output_path = os.getcwd() + os.sep + self.config.get('Paths', 'output')

    def config_load_email(self):
        """Load the settings from email section."""
        self.address = self.config.get('Email','address')
        self.password = self.config.get('Email','password')
        self.mailbox = self.config.get('Email', 'mailbox')

    def config_load_qif(self):
        """Load the settings from qif section."""
        self.qif_filenames = dict(self.config.items('Qif_Filenames'))
        self.qif_types = dict(self.config.items('Qif_Types'))
        self.qif_assets = dict(self.config.items('Qif_Assets'))
        self.qif_liabilities = dict(self.config.items('Qif_Liabilities'))
        self.qif_revenues = dict(self.config.items('Qif_Revenues'))
        self.qif_expenses = dict(self.config.items('Qif_Expenses'))

    def config_setup(self):
        """Setup configuration settings and return if successful."""
        if not os.path.isfile(self.file_config):
            self.config_create_default()
            self.log.info('Created default config file. Please enter your information.')
            return False
        elif self.config_is_valid():
            self.config_load()
            return True
        else:
            return False

    # Initialization
    def main(self):
        """Setup and process email inbox."""
        # TODO: move check for folders up here
        self.log = logger.Logger('Powl')
        config_successful = self.config_setup()
        if config_successful:
            self.check_for_existing_folders()
            self.initialize_modules()
            self.process_inbox()

    def check_for_existing_folders(self):
        """Check if folders exist and if not create them."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def initialize_modules(self):
        """Intialize modules used for doing various actions."""
        self.transaction = transaction.Transaction(self.output_path)
    
if __name__ == '__main__':
    Powl().main()
