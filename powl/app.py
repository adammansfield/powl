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
from powl.parser import MessageParser

class Controller:

    # Email Processing
    def start(self):
        """Process mailbox to do the spceified actions of each message."""
        mail_list = self._mail.get_mail_list()
        for message, date in mail_list:
            action, data = self._parser.parse_message(message)
            self._actions.do_action(action, data, date)
            

    # Action Processing
    def process_miscellaneous(self, data, date):
        """Write miscellaneous message to file."""
        filename = os.path.join(self.config.output_dir, 'miscellaneous.txt')
        output.append(filename, data)
        logger.info('MISC\t%s', data)

    def process_transaction(self, params, date):

    




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
        self.config.read()

    def _load_mail(self):
        """Setup the mail module with custom creditials."""
        self._mail = Mail(self._config.server,
                          self._config.address,
                          self._config.password,
                          self._config.mailbox)
        self._mail.setup()

    def _load_processors(self):
        """Load the processors with custom config settings."""
        self._actions = Actions(self._config)
        self._parser = MessageParser()

    # INITIALIZATION
    def __init__(self):
        """Setup and process email inbox."""
        logger.initialize(logger.FORMAT_WEEKLY)
        self._load_config()
        self._create_directories()
        logger.set_file_handler(self.config.log_dir)
        self._load_mail()
        self._load_processors()
        self._create_transaction_templates()

