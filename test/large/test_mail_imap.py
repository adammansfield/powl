#!/usr/bin/env python
import copy
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


class _SimpleMessage(object):
    """
    A simplified email.message.Message object.
    """

    def __init__(self):
        self.body = None
        self.date = None

    def __eq__(self, other):
        # For debugging purposes.
        if self.body != other.body:
            print
            print repr(self) + " != " + repr(other)
            print "  self.body != other.body"
            print "  " + self.body + " != " + other.body
            return False

        if self.date != other.date:
            print
            print repr(self) + " != " + repr(other)
            print "  self.date != other.date"
            print "  " + self.date + " != " + other.date
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class ImapMailTest(unittest.TestCase):

    def _from_messages(self, messages):
        """
        Returns a list _SimpleMessage from email.message.Message.
        """
        simple_messages = []
        for message in messages:
            message_helper = actionretriever.MessageHelper(message)
            struct_time = message_helper.get_date()

            body = message_helper.get_body()
            date = time.strftime("%Y-%m-%dT%H:%M", struct_time)

            simple_message = _SimpleMessage()
            simple_message.body = body
            simple_message.date = date
            simple_messages.append(simple_message)
        return simple_messages

    def _from_tuples(self, tuples):
        """
        Returns a list _SimpleMessage from list of (date, body).
        """
        simple_messages = []
        for date, body in tuples:
            simple_message = _SimpleMessage()
            simple_message.body = body
            simple_message.date = date
            simple_messages.append(simple_message)
        return simple_messages

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

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = self._imap._ERRMSG_SERVER_NOT_FOUND.format(
            server)
        self.assertEqual(expected_errmsg, actual_errmsg)

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

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = self._imap._ERRMSG_TIMEOUT.format(
            imapconfig.not_imap_server)
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__called_before_connect(self):
        """
        Test that login throws if called before connect.
        """
        with self.assertRaises(ValueError) as context:
            self._imap.login(imapconfig.user, imapconfig.password)

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = self._imap._ERRMSG_NOT_CONNECTED
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__invalid_credentials(self):
        """
        Test that login throws if invalid email and password are given.
        """
        self._imap.connect(imapconfig.server)
        with self.assertRaises(Exception) as context:
            self._imap.login("invaliduser", "invalidpassword")

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = self._imap._ERRMSG_INVALID_CREDENTIALS
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__login__invalid_mailbox(self):
        """
        Test that login throws if it selects an invalid mailbox.
        """
        mailbox = "invaild_mailbox"
        imap = actionretriever.ImapMail(mailbox, imapconfig.timeout)
        imap.connect(imapconfig.server)
        with self.assertRaises(ValueError) as context:
            imap.login(imapconfig.user, imapconfig.password)

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = self._imap._ERRMSG_INVALID_MAILBOX.format(
            mailbox)
        self.assertEqual(expected_errmsg, actual_errmsg)

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
            self._imap.get_messages()

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = self._imap._ERRMSG_NOT_CONNECTED
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__get_messages__called_before_login(self):
        """
        Test that get_messages() throws if called before login.
        """
        self._imap.connect(imapconfig.server)

        with self.assertRaises(ValueError) as context:
            self._imap.get_messages()

        actual_errmsg = exception.get_message(context.exception)
        expected_errmsg = self._imap._ERRMSG_NOT_LOGGED_IN
        self.assertEqual(expected_errmsg, actual_errmsg)

    def test__get_messages__success(self):
        """
        Test we are able to get a message and its date.
        This assumes that there is only two unread emails on the server
        in the mailbox specified.
        """
        self._imap.connect(imapconfig.server)
        self._imap.login(imapconfig.user, imapconfig.password)

        actual_messages = self._imap.get_messages()
        actual_simple_messages = self._from_messages(actual_messages)

        expected_tuples = imapconfig.expected_emails
        expected_simple_messages = self._from_tuples(expected_tuples)

        self.assertEqual(len(expected_simple_messages),
                         len(actual_simple_messages))

        expected_simple_messages.sort(key=lambda x: x.date)
        actual_simple_messages.sort(key=lambda x: x.date)

        combined_list = zip(expected_simple_messages, actual_simple_messages)
        for expected, actual in combined_list:
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

