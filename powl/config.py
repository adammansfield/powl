#!/usr/bin/env python
"""Load configuration settings for powl."""
import ConfigParser
import os
import textwrap

class Config:
    """Class for processing custom powl config file for settings."""

    # CONSTANTS
    config_filepath = 'config.cfg'
    _transaction_dir = 'transactions'
    _log_dir = 'logs'
    
    # DEFAULTS
    _default_server = 'imap.gmail.com'
    _default_mailbox = 'inbox'
    _default_output_dir = os.path.join(os.getcwd(), 'output')

    # CONFIG SECTIONS AND KEYS
    _email_section = 'Email'
    _email_server = 'server'
    _email_address = 'address'
    _email_password = 'password'
    _email_mailbox = 'mailbox'
    _folders_section = 'Folders'
    _folders_output = 'output'
    _accounting_filenames_section = 'Accounting Filenames'
    _accounting_types_section = 'Accounting Types'
    _assets_section = 'Assets'
    _liabilities_section = 'Liabilities'
    _revenues_section = 'Revenues'
    _expenses_section = 'Expenses'

    # CONFIG FILE
    _config_section_keys = {
        'email_section': _email_section,
        'email_server': _email_server,
        'email_address': _email_address,
        'email_password': _email_password,
        'email_mailbox': _email_mailbox,
        'folders_section': _folders_section,
        'folders_output': _folders_output,
        'accounting_filenames_section': _accounting_filenames_section,
        'accounting_types_section': _accounting_types_section,
        'assets_section': _assets_section,
        'liabilities_section': _liabilities_section,
        'revenues_section': _revenues_section,
        'expenses_section': _expenses_section
    }
    config_template = textwrap.dedent("""\
        [{email_section}]
        {email_server}=
        {email_address}=
        {email_password}=
        {email_mailbox}=

        [{folders_section}]
        {folders_output}=

        [{accounting_filenames_section}]

        [{accounting_types_section}]

        [{assets_section}]

        [{liabilities_section}]

        [{revenues_section}] 

        [{expenses_section}]""".format(**_config_section_keys) 
    )

    # FILE I/O
    def _get_configparser(self):
        """Read from config file to get config parser."""
        self._config = ConfigParser.ConfigParser()
        try:
            with open(self.config_filepath) as fp:
                self._config.readfp(fp)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # LOADING SETTINGS
    def _load_all_settings(self):
        """Load all the settings from each subsection."""
        self._load_email_settings()
        self._load_folders_settings()
        self._load_qif_settings()

    def _load_email_settings(self):
        """Load the settings from the email section."""
        self.server = self._config.get(self._email_section,
                                       self._email_server)
        if not self.server:
            self.server = self._default_server
        self.address = self._config.get(self._email_section,
                                        self._email_address)
        self.password = self._config.get(self._email_section,
                                         self._email_password)
        self.mailbox = self._config.get(self._email_section,
                                        self._email_mailbox)
        if not self.mailbox:
            self.mailbox = self._default_mailbox

    def _load_folders_settings(self):
        """Load the settings from the paths section."""
        self.output_dir = self._config.get(self._folders_section,
                                           self._folders_output)
        if not self.output_dir:
            self.output_dir = self._default_output_dir
        self.log_dir = os.path.join(self.output_dir, self._log_dir)
        self.transaction_dir = os.path.join(self.output_dir, self._transaction_dir)
        self.directories = [
            self.output_dir,
            self.log_dir,
            self.transaction_dir
        ]

    def _load_qif_settings(self):
        """Load the settings from the qif sections."""
        self.qif_filenames = dict(
            self._config.items(self._accounting_filenames_section)
        )
        self.qif_types = dict(
            self._config.items(self._accounting_types_section)
        )
        self.qif_assets = dict(
            self._config.items(self._assets_section)
        )
        self.qif_liabilities = dict(
            self._config.items(self._liabilities_section)
        )
        self.qif_revenues = dict(
            self._config.items(self._revenues_section)
        )
        self.qif_expenses = dict(
            self._config.items(self._expenses_section)
        )

    # READING AND LOADING
    def read(self):
        """Check if config exists and load all settings."""
        self._get_configparser()
        self._load_all_settings()
