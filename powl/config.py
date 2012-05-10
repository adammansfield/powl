#!/usr/bin/env python
"""Load configuration settings for powl."""
import ConfigParser
import os
import textwrap

class Config:
    """Class for processing custom powl config file for settings."""

    # DEFAULTS
    default_filepath = 'config.cfg'
    default_mailbox = 'inbox'
    default_output_dir = os.getcwd() + os.sep + 'output'

    # CONFIG FILE
    section_email = {
        'email': 'Email',
        'address': 'address',
        'password': 'password',
        'mailbox': 'mailbox'
    }
    section_folders = { 
        'folders': 'Folders',
        'output': 'output'
    }
    section_accounting = {
        'accounting_filenames': 'Accounting Filenames',
        'accounting_types': 'Accounting Types',
        'assets': 'Assets',
        'liabilities': 'Liabilities',
        'revenues': 'Revenues',
        'expenses': 'Expenses'
    }
    config_sections = dict(section_email.items() +
                           section_folders.items() +
                           section_accounting.items())
    # TODO: add comments to default config file on how to fill out.
    config_file_layout = textwrap.dedent("""\
        [{email}]
        {address}=
        {password}=
        {mailbox}=

        [{folders}]
        {output}=

        [{accounting_filenames}]

        [{accounting_types}]

        [{assets}]

        [{liabilities}]

        [{revenues}] 

        [{expenses}]""".format(**config_sections)
    )

    # CONFIG FILE
    def read_config_file(self):
        """Check if config exists and load all settings."""
        self.create_default_config_file_if_missing()
        self.get_configparser()
        self.load_all_settings()
        self.set_unknowns_to_defaults()
        self.create_output_dir_if_missing()

    def get_configparser(self):
        """Get config parser and read from file."""
        self.config = ConfigParser.ConfigParser()
        with open(self.filepath) as fp:
            self.config.readfp(fp)

    # MISSING FILES AND FOLDERS
    def create_default_config_file_if_missing(self):
        """Create a default config file if it is missing."""
        if not os.path.isfile(self.filepath):
            file = open(self.filepath, 'w')
            file.write(self.config_file_layout)
            file.close()

    def create_output_dir_if_missing(self):
        """Create the output directory if it is missing."""
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

    # LOADING SETTINGS
    def load_all_settings(self):
        """Load all the settings from each subsection."""
        self.load_email_settings()
        self.load_folders_settings()
        self.load_qif_settings()

    def load_email_settings(self):
        """Load the settings from the email section."""
        email_section = self.section_email['email']
        address_key = self.section_email['address']
        password_key = self.section_email['password']
        mailbox_key = self.section_email['mailbox']
        self.address = self.config.get(email_section, address_key)
        self.password = self.config.get(email_section, password_key)
        self.mailbox = self.config.get(email_section, mailbox_key)

    def load_folders_settings(self):
        """Load the settings from the paths section."""
        folders_section = self.section_folders['folders']
        output_key = self.section_folders['output']
        self.output_dir = self.config.get(folders_section, output_key)

    def load_qif_settings(self):
        """Load the settings from the qif sections."""
        filenames_section = self.section_accounting['accounting_filenames']
        types_section = self.section_accounting['accounting_types']
        assets_section = self.section_accounting['assets']
        liabilities_section = self.section_accounting['liabilities']
        expenses_section = self.section_accounting['expenses']
        revenues_section = self.section_accounting['revenues']
        self.qif_filenames = dict(self.config.items(filenames_section))
        self.qif_types = dict(self.config.items(types_section))
        self.qif_assets = dict(self.config.items(assets_section))
        self.qif_liabilities = dict(self.config.items(liabilities_section))
        self.qif_revenues = dict(self.config.items(revenues_section))
        self.qif_expenses = dict(self.config.items(expenses_section))

    def set_unknowns_to_defaults(self):
        """Set blank setting to the defaults."""
        if not self.mailbox:
            self.mailbox = self.default_mailbox
        if not self.output_dir:
            self.output_dir = self.default_output_dir

    # INITIALIZATION
    def __init__(self, filepath=''):
        """Initialize powl config and set filepath if custom."""
        if filepath:
            self.filepath = filepath
        else:
            self.filepath = self.default_filepath
