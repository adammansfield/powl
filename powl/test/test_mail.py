#!/usr/bin/env python
import socket
import unittest
from powl.config import Config
from powl.mail import Mail

class MailTest(unittest.TestCase):
    # TEST DATA
    empty_server = ''
    empty_address = ''
    empty_password = ''
    fake_server = 'foo'
    fake_address = 'Btu72Bu7atu'
    fake_password = '8u89HuhiOUU'
    gmail_server = 'imap.gmail.com'
    nonimap_server = 'google.ca'

    # IMAP SETUP
    def test_imap_empty(self):
        """Test imap with an empty server."""
        mail = Mail(self.empty_server, 
                    self.empty_address,
                    self.empty_password)
        expected = Mail.EmptyServer
        self.assertRaises(expected, mail._get_imap)

    def test_imap_success(self):
        """Test imap connection success."""
        mail = Mail(self.gmail_server,
                    self.empty_address,
                    self.empty_password)
        try:
            mail._get_imap()
        except Exception as e:
            self.fail(e)

    def test_imap_timeout(self):
        """Test imap timeout."""
        mail = Mail(self.nonimap_server,
                    self.empty_address,
                    self.empty_password)
        expected = Mail.ServerTimedOutError
        self.assertRaises(expected, mail._get_imap)

    def test_imap_unknown(self):
        """Test imap with an unknown address."""
        mail = Mail(self.fake_server,
                    self.empty_address,
                    self.empty_password)
        expected = Mail.ServerUnknownError
        self.assertRaises(expected, mail._get_imap)

    # LOGIN
    def test_login_fail(self):
        """Test login with wrong creditionals."""
        mail = Mail(self.gmail_server, 
                    self.fake_address,
                    self.fake_password)
        mail._get_imap()
        expected = Mail.LoginFailure
        self.assertRaises(expected, mail._login)

    def test_login_empty_address(self):
        """Test login with an empty address."""
        mail = Mail(self.empty_server,
                    self.empty_address,
                    self.fake_password)
        expected = Mail.EmptyAddress
        self.assertRaises(expected, mail._login)

    def test_login_empty_password(self):
        """Test login with a empty password."""
        mail = Mail(self.empty_server,
                    self.fake_address,
                    self.empty_password)
        expected = Mail.EmptyPassword
        self.assertRaises(expected, mail._login)

    def test_login_config(self):
        """Test login with config creditials and should succeed if correct."""
        try:
            config = Config()
            config.read()
        except Exception as e:
            logger.error("Config.cfg was not found for intergation test.")
            self.fail(e)
        mail = Mail(config.server,
                    config.address,
                    config.password)
        try:
            mail._get_imap()
            mail._login()
        except Exception as e:
            self.fail("Unexpected exception." + str(e))

if __name__ == '__main__':
    unittest.main()
