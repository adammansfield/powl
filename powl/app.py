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
from powl.actions import Actions
from powl.config import Config
from powl.mail import Mail
from powl.parser import Parser
from powl.transaction import Transaction

class App:

    # Email Processing
    def start(self):
        """Process mailbox to do the spceified actions of each message."""
        self._mail.setup()
        mail_list = self._mail.get_mail_list()
        for message, date in mail_list:
            action, data = self._parser.parse_message(message)
            self._actions.do_action(action, data, date)

    # FILE I/O
    # TODO: this section move to data.py
    def _create_directories(self):
        """Create the configured directories if they do not exist."""
        output.makedir(self._config.directories)

    def _create_transaction_templates(self):
        """Create transaction templates if files do not exist."""
        templates = self._transaction.get_templates()
        for filename, template in templates:
            filepath = os.path.join(self._config.transaction_dir, filename)
            if not os.path.isfile(filepath):
                output.write(filepath, template)
         
    # SETUP
    def _setup_logger(self):
        """Set logger format and set file output."""
        logger.initialize(logger.FORMAT_WEEKLY)
        logger.set_file_handler()

    def _setup_config(self):
        """Check for config file and load settings."""
        self._config = Config()
        self._config.check_file()
        self._config.read()

    def _setup_mail(self):
        """Setup mail with custom creditials."""
        server = self._config.server
        address = self._config.address
        password = self._config.password
        mailbox = self._config.mailbox
        self._mail = Mail(server, address, password, mailbox)

    def _setup_transaction(self):
        """Setup transaction processor with custom accounts."""
        self._transaction = Transaction(self._config.qif_filenames,
                                        self._config.qif_types,
                                        self._config.qif_assets,
                                        self._config.qif_liabilities,
                                        self._config.qif_revenues,
                                        self._config.qif_expenses)

    def _setup_actions(self):
        """Setup actions and pass necessary objects."""
        self._actions = Actions(self._mail, 
                                self._transaction,
                                self._config.output_dir,
                                self._config.transaction_dir)

    def _setup_parser(self):
        """Setup parser."""
        self._parser = Parser()

    # INITIALIZATION
    def __init__(self):
        """Setup objects necessary for processing the email inbox."""
        self._setup_logger()
        self._setup_config()
        self._setup_transaction()
        self._create_directories() # TODO: move to data.py
        self._create_transaction_templates() # TODO: move to data.py
        self._setup_mail()
        self._setup_actions()
        self._setup_parser()
