#!/usr/bin/env python
import socket
import time
import unittest
from powl import actionretriever
from powl import exception

try:
    from test.config import imapconfig
except ImportError:
    import os
    import textwrap
    cfg_path = os.path.join("test", "config", "imapconfig.py")
    with open(cfg_path, 'a') as cfg_file:
        template = textwrap.dedent(
            """\
            # Server Address
            server = "<enter server here>"

            # Email Address
            user = "<enter user here>"

            # Email Password
            password = "<enter password here>"

            # Mailbox folder
            mailbox = "<enter mailbox here>"

            # Timeout in seconds
            timeout = 1

            # Server that is not an IMAP server
            not_imap_server = "<enter not imap server here>"

            # Body of the email
            first_email_body = "<enter body of 1st email here> 

            # Date of the email in YYYY-MM-DD
            first_email_date = "<enter date of 1st email here> 

            # Body of the email
            second_email_body = "<enter body of 2nd email here> 

            # Date of the email in YYYY-MM-DD
            second_email_date = "<enter date of 2nd email here> 
            """)
        cfg_file.write(template)
    raise SystemExit("Need to fill out test/config/imapconfig.py")


class ImapMailTest(unittest.TestCase):

    def setUp(self):
        self._imap = actionretriever.ImapMail(imapconfig.mailbox,
                                              imapconfig.timeout)

    def test__connect__server_not_found(self):
        """
        Test that connect throws if server not found.
        """
        server = "non-existant server"
        with self.assertRaises(IOError) as context:
            self._imap.connect(server)

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_SERVER_NOT_FOUND.format(
            server)
        self.assertEqual(expected_message, actual_message)

    def test__connect__success(self):
        """
        Test that IMAP object successfully connects to server.
        """
        self._imap.connect(imapconfig.server)

    def test__connect__timeout(self):
        """
        Test that connect throws if server connection has timed out.
        """
        with self.assertRaises(IOError) as context:
            self._imap.connect(imapconfig.not_imap_server)

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_TIMEOUT.format(
            imapconfig.not_imap_server)
        self.assertEqual(expected_message, actual_message)

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

    def test__get_messages__called_before_connect(self):
        """
        Test that get_messages() throws if called before connect.
        """
        with self.assertRaises(ValueError) as context:
            self._imap.get_message_id_list()

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_NOT_CONNECTED
        self.assertEqual(expected_message, actual_message)

    def test__get_messages__called_before_login(self):
        """
        Test that get_messages() throws if called before login.
        """
        self._imap.connect(imapconfig.server)

        with self.assertRaises(ValueError) as context:
            self._imap.get_message_id_list()

        actual_message = exception.get_message(context.exception)
        expected_message = self._imap._ERROR_NOT_LOGGED_IN
        self.assertEqual(expected_message, actual_message)

    def test__get_messages__success(self):
        """
        Test we are able to get a message and its date.
        This assumes that there is only one unread email on the server
        in the mailbox specified.
        """
        self._imap.connect(imapconfig.server)
        self._imap.login(imapconfig.user, imapconfig.password)
        self.fail("test not finished")


if __name__ == '__main__':
    unittest.main()

