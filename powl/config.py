#!/usr/bin/env python
"""Load and store configuration settings."""
import ConfigParser
import os
import textwrap
import powl.output as output

class Config:

    # CONSTANTS
    _config_filename = 'config.cfg'
    _transaction_dir = 'transactions'
    
    _default_server = 'imap.gmail.com'
    _default_mailbox = 'inbox'
    _default_output_dir = os.path.join(os.getcwd(), 'output')

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
    _config_template = textwrap.dedent("""\
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

    def __init__(self, folder):
        """
        Initialize and set config folder.

        Args:
            folder (powl.filesystem.Folder): Folder containing config files.
        """
        self._folder = folder

        if folder.file_exists(self._config_filename):
            file_object = folder.get_file(self._config_filename)
        else:
            file_object = folder.get_file(self._config_filename)
            file_object.write(self._config_template)

        self._config = ConfigParser.ConfigParser()
        with open(file_object.path) as fp:
            self._config.readfp(fp)

        self._load_accounting_settings()
        self._load_email_settings()
        self._load_folders_settings()

    def _load_accounting_settings(self):
        """Load the settings from the accounting sections."""
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
        self.transaction_dir = os.path.join(self.output_dir, self._transaction_dir)
        self.directories = [
            self.output_dir,
            self.transaction_dir
        ]
