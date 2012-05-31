#!/usr/bin/env python
import socket
import unittest
from powl.config import Config
from powl.mail import Mail

class MailTest(unittest.TestCase):
    server_gmail = 'imap.gmail.com'
    server_timeout = 'google.ca'
    server_unknown = 'foo'

    def test_imap_success(self):
        """Test imap connection success."""
        mail = Mail(self.server_gmail, '', '')
        try:
            mail._get_imap()
        except:
            self.fail("Unexpected exception raised.")

    def test_imap_timeout(self):
        """Test imap timeout."""
        mail = Mail(self.server_timeout, '', '')
        expected = Mail.ServerTimedOutError
        self.assertRaises(expected, mail._get_imap)

    def test_imap_unknown(self):
        """Test imap with an unknown address."""
        mail = Mail(self.server_unknown, '', '')
        expected = Mail.ServerUnknownError
        self.assertRaises(expected, mail._get_imap)

    def test_login_fail(self):
        """Test login with wrong creditionals."""
        pass

if __name__ == '__main__':
    unittest.main()
