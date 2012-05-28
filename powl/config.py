#!/usr/bin/env python
"""Load configuration settings for powl."""
import ConfigParser
import os
import textwrap

class Config:
    """Class for processing custom powl config file for settings."""

    # DEFAULTS
    _default_filepath = 'config.cfg'
    _default_mailbox = 'inbox'
    _default_output_dir = os.join(os.getcwd(), 'output')

    # CONSTANTS
    _transaction_dir = 'transactions'
    _log_dir = 'logs'

    # CONFIG SECTIONS AND KEYS
    _email_section = 'Email'
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
        'email_section': self._email_section,
        'email_address': self._email_address,
        'email_password': self._email_password,
        'email_mailbox': self._email_mailbox
        'folders_section': self._folders_section,
        'folders_output': self._folders_output
        'accounting_filenames_section': self._accounting_filenames_section,
        'accounting_types_section': self._accounting_types_section,
        'assets_section': self._assets_section,
        'liabilities_section': self._liabilities_section,
        'revenues_section': self._revenues_section,
        'expenses_section': self._expenses_section
    }
    config_template = textwrap.dedent("""\
        [{email_section}]
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

        [{expenses_section}]""".format(_config_section_keys) 
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
        self.address = self._config.get(self._email_section,
                                        self._email_address)
        self.password = self._config.get(self._email_section,
                                         self._email_password)
        self.mailbox = self._config.get(self._email_section,
                                        self._email_mailbox)

    def _load_folders_settings(self):
        """Load the settings from the paths section."""
        self.output_dir = self.config.get(self._folders_section,
                                          self._folders_output)
        self.log_dir = os.join(self.output_dir, self._log_dir)
        self.qif_dir = os.join(self.output_dir, self._transactions_dir)
        self.directories = [
            self.output_dir,
            self.log_dir,
            self.qif_dir
        ]

    def _load_qif_settings(self):
        """Load the settings from the qif sections."""
        self.qif_filenames = dict(
            self.config.items(self._accounting_filenames_section)
        )
        self.qif_types = dict(
            self.config.items(self._accounting_types_section)
        )
        self.qif_assets = dict(
            self.config.items(self._assets_section)
        )
        self.qif_liabilities = dict(
            self.config.items(self._liabilities_section)
        )
        self.qif_revenues = dict(
            self.config.items(self._revenues_section)
        )
        self.qif_expenses = dict(
            self.config.items(self._expenses_section)
        )

    # SETTING DEFAULTS
    def _set_unknowns_to_defaults(self):
        """Set blank setting to the defaults."""
        if not self.mailbox:
            self.mailbox = self._default_mailbox
        if not self.output_dir:
            self.output_dir = self._default_output_dir

    # READING AND LOADING
    def read(self):
        """Check if config exists and load all settings."""
        self._get_configparser()
        self._load_all_settings()
        self._set_unknowns_to_defaults()
