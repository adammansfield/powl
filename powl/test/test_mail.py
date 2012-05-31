#!/usr/bin/env python
import socket
import unittest
from powl.mail import Mail

class MailTest(unittest.TestCase):
    server_notexist = 'blah'
    server_notimap = 'google.ca'
    
    def test_imap_notfound(self):
        server = self.server_notimap
        address = ''
        password = ''
        mail = Mail(server, address, password)
        expected = Mail.ServerTimedOutError
        self.assertRaises(expected, mail._get_imap)

    def test_imap_unknown(self):
        server = self.server_notexist
        address = ''
        password = ''
        mail = Mail(server, address, password)
        expected = Mail.ServerUnknownError
        self.assertRaises(expected, mail._get_imap)

if __name__ == '__main__':
    unittest.main()
