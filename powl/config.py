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
    default_sections_and_keys = {
        'email': 'Email',
        'address': 'address',
        'password': 'password',
        'mailbox': 'mailbox',
        'folders': 'Folders',
        'output': 'output',
        'account_filenames': 'Accounting Filenames',
        'account_types': 'Accounting Types',
        'assets': 'Assets',
        'liabilities': 'Liabilities',
        'revenues': 'Revenues',
        'expenses': 'Expenses'
    }
    default_config = textwrap.dedent("""\
        [{email}]
        {address}=
        {password}=
        {mailbox}=

        [{folders}]
        {output}=

        [{account_filenames}]

        [{account_types}]

        [{assets}]

        [{liabilities}]

        [{revenues}] 

        [{expenses}]""".format(**default_sections_and_keys)
    )
    
    def create_default_config(self):
        """Create a default config file."""
        if not os.path.isfile(self.filepath):
            file = open(self.filepath, 'a')
            file.write(self.default)
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
        self.config_load_email()
        self.config_load_qif()
        self.output_path = os.getcwd() + os.sep + self.config.get('Paths', 'output')


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


    # 
    def load_config(self):
    """Check if config exists and load all settings."""
        if not os.path.isfile(self.filepath)
            self.create_default_config()
        self.load_all_settings()



    # LOADING SETTINGS
    def load_all_settings(self):
        """Load all the settings from each subsection."""
        self.load_email_settings()
        self.load_paths_settings()
        self.load_qif_settings()

    def load_email_settings(self):
        """Load the settings from the email section."""
        self.address = self.config.get('Email','address')
        self.password = self.config.get('Email','password')
        self.mailbox = self.config.get('Email', 'mailbox')

    def load_paths_settings(self):
        """Load the settings from the paths section."""
        self.output_path = os.getcwd() + os.sep + self.config.get('Paths', 'output')

    def load_qif_settings(self):
        """Load the settings from the qif sections."""
        self.qif_filepaths = dict(self.config.items('Qif_Filenames'))
        self.qif_types = dict(self.config.items('Qif_Types'))
        self.qif_assets = dict(self.config.items('Qif_Assets'))
        self.qif_liabilities = dict(self.config.items('Qif_Liabilities'))
        self.qif_revenues = dict(self.config.items('Qif_Revenues'))
        self.qif_expenses = dict(self.config.items('Qif_Expenses'))

    # INITIALIZATION
    def __init__(self, filepath=''):
        """Initialize and read powl config. Set filepath if custom."""
        if filepath:
            self.filepath = filepath
        else:
            self.filepath = self.default_filepath
        self.config = ConfigParser.ConfigParser()
        with open(self.filepath) as fp:
            self.config.readfp(fp)
