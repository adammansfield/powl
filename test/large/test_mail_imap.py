#!/usr/bin/env python
import time
import unittest
from powl import exception
from powl import mail

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

            # Expected emails (order does not matter)
            # list of date, body
            #  date: str as YYYY-MM-DDTHH::MM (must be unique in list)
            #  body: str as plain text
            expected_emails = [
                ("YYYY-MM-DDTHH:MM", "body"),
                ("2014-12-31T15:30", "hello"),
            ]
            """)
        cfg_file.write(template)
    raise SystemExit("Need to fill out test/config/imapconfig.py")


class ImapMailTest(unittest.TestCase):

    def setUp(self):
        self._imap = mail.ImapMail(imapconfig.mailbox,
                                              imapconfig.timeout)

    def test__connect__empty_server(self):
        server = ""
        with self.assertRaises(ValueError) as context:
            self._imap.connect(server)

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_EMPTY_SERVER
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__connect__server_not_found(self):
        server = "non-existant server"
        with self.assertRaises(IOError) as context:
            self._imap.connect(server)

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_SERVER_NOT_FOUND.format(
            server)
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__connect__successfully(self):
        self._imap.connect(imapconfig.server)

    def test__connect__timeout(self):
        with self.assertRaises(IOError) as context:
            self._imap.connect(imapconfig.not_imap_server)

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_TIMEOUT.format(
            imapconfig.not_imap_server)
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__called_before_connect_fails(self):
        with self.assertRaises(ValueError) as context:
            self._imap.login(imapconfig.user, imapconfig.password)

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_NOT_CONNECTED
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__empty_password(self):
        self._imap.connect(imapconfig.server)

        with self.assertRaises(ValueError) as context:
            self._imap.login(user="user", password="")

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_EMPTY_PASSWORD
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__empty_user(self):
        self._imap.connect(imapconfig.server)

        with self.assertRaises(ValueError) as context:
            self._imap.login(user="", password="password")

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_EMPTY_USER
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__invalid_credentials(self):
        self._imap.connect(imapconfig.server)
        with self.assertRaises(Exception) as context:
            self._imap.login("invaliduser", "invalidpassword")

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_INVALID_CREDENTIALS
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__invalid_mailbox(self):
        mailbox = "invaild_mailbox"
        imap = mail.ImapMail(mailbox, imapconfig.timeout)
        imap.connect(imapconfig.server)
        with self.assertRaises(ValueError) as context:
            imap.login(imapconfig.user, imapconfig.password)

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_INVALID_MAILBOX.format(
            mailbox)
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__successfully(self):
        self._imap.connect(imapconfig.server)
        self._imap.login(imapconfig.user, imapconfig.password)

    def test__get_messages__called_before_connect_fails(self):
        with self.assertRaises(ValueError) as context:
            self._imap.get_messages()

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_NOT_CONNECTED
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__get_messages__called_before_login_fails(self):
        self._imap.connect(imapconfig.server)

        with self.assertRaises(ValueError) as context:
            self._imap.get_messages()

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = mail._ERRMSG_NOT_LOGGED_IN
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__get_messages__successfully(self):
        """
        This assumes that there is unread emails on the server
        that match what is specified in the imapconfig.
        """
        self._imap.connect(imapconfig.server)
        self._imap.login(imapconfig.user, imapconfig.password)
        actual_messages = self._imap.get_messages()

        expected_tuples = imapconfig.expected_emails
        self.assertEqual(len(expected_tuples), len(actual_messages))

        expected_tuples.sort(key=lambda x: x[0])
        actual_messages.sort(key=lambda x: x.date)

        combined_list = zip(expected_tuples, actual_messages)
        for expected, actual in combined_list:
            actual_date_iso8601 = time.strftime("%Y-%m-%dT%H:%M", actual.date)
            self.assertEqual(expected[0], actual_date_iso8601)
            self.assertEqual(expected[1], actual.body)


if __name__ == '__main__':
    unittest.main()

