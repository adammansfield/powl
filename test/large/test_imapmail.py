#!/usr/bin/env python
import os
import socket
import time
import unittest
from powl import actionretriever
from powl import exception
try:
    from test.config import imapconfig
except ImportError:
    cfg_path = os.path.join("test", "config", "imapconfig.py")
    with open(cfg_path, 'a') as cfg_file:
        cfg_file.write("# Server Address" + os.linesep)
        cfg_file.write("server = \"<enter server here>\"" + os.linesep)
        cfg_file.write("# Email Address" + os.linesep)
        cfg_file.write("user = \"<enter user here>\"" + os.linesep)
        cfg_file.write("# Email Password" + os.linesep)
        cfg_file.write("password = \"<enter password here>\"" + os.linesep)
        cfg_file.write("# Mailbox folder" + os.linesep)
        cfg_file.write("mailbox = \"<enter mailbox here>\"" + os.linesep)
        cfg_file.write("# Timeout in seconds" + os.linesep)
        cfg_file.write("timeout = 1" + os.linesep)
    from test.config import imapconfig


class ImapMailTest(unittest.TestCase):

    def setUp(self):
        self._imap = actionretriever.ImapMail(imapconfig.mailbox,
                                              imapconfig.timeout)

    def test__connect__success(self):
        """
        Test that IMAP object successfully connects to server.
        """
        self._imap.connect(imapconfig.server)

    def test__login__called_before_connect(self):
        """
        Test that login throws if called before connect.
        """
        with self.assertRaises(ValueError) as context:
            self._imap.login(imapconfig.user, imapconfig.password)

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_NOT_CONNECTED
        self.assertEqual(expected_message, actual_message)

    def test__login__invalid_credentials(self):
        """
        Test that login throws if invalid email and password are given.
        """
        self._imap.connect(imapconfig.server)
        with self.assertRaises(Exception) as context:
            self._imap.login(imapconfig.user, "invalidpassword")

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_INVALID_CREDENTIALS
        self.assertEqual(expected_message, actual_message)

    def test__login__invalid_mailbox(self):
        """
        Test that login throws if it selects an invalid mailbox.
        """
        mailbox = "invaild_mailbox"
        imap = actionretriever.ImapMail(mailbox, imapconfig.timeout)
        imap.connect(imapconfig.server)
        with self.assertRaises(ValueError) as context:
            imap.login(imapconfig.user, imapconfig.password)

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_INVALID_MAILBOX.format(
            mailbox)
        self.assertEqual(expected_message, actual_message)

    def test__login__success(self):
        """
        Test that login with valid credentials is successful.
        """
        self._imap.connect(imapconfig.server)
        self._imap.login(imapconfig.user, imapconfig.password)

    def test__get_message_id_list__called_before_connect(self):
        """
        Test that get_message_id_list() throws if called before connect.
        """
        with self.assertRaises(ValueError) as context:
            self._imap.get_message_id_list()

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_NOT_CONNECTED
        self.assertEqual(expected_message, actual_message)


if __name__ == '__main__':
    unittest.main()

