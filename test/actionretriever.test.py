#!/usr/bin/env python
"""Tests for powl.actionretriever."""
import unittest
from powl import actionretriever
from powl import exception

class MailRetrieverTest(unittest.TestCase):

    def setUp(self):
        self._mock_server = "mail.test.com"
        self._mock_address = "test@test.com"
        self._mock_password = "mockpassword"

    def test__init__empty_server(self):
        """
        Test exception is thrown if given server address is empty.
        """
        with self.assertRaises(ValueError) as context:
            actionretriever.MailRetriever("", # todo: replace with MockMail
                                          "",
                                          self._mock_address,
                                          self._mock_password)
        expected_message = actionretriever.MailRetriever._ERROR_EMPTY_SERVER
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__init__empty_address(self):
        """
        Test exception is thrown if given email address is empty.
        """
        with self.assertRaises(ValueError) as context:
            actionretriever.MailRetriever("", # todo: replace with MockMail
                                          self._mock_server,
                                          "",
                                          self._mock_password)
        expected_message = actionretriever.MailRetriever._ERROR_EMPTY_ADDRESS
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)

    def test__init__empty_password(self):
        """
        Test exception is thrown if given email password is empty.
        """
        with self.assertRaises(ValueError) as context:
            actionretriever.MailRetriever("", # todo: replace with MockMail
                                          self._mock_server,
                                          self._mock_address,
                                          "")
        expected_message = actionretriever.MailRetriever._ERROR_EMPTY_PASSWORD
        actual_message = exception.get_message(context.exception)
        self.assertEqual(expected_message, actual_message)


#    # IMAP SETUP
#    def test_imap_empty(self):
#        """Test imap with an empty server."""
#        mail = Mail(self.empty_server, 
#                    self.empty_address,
#                    self.empty_password)
#        expected = Mail.EmptyServer
#        self.assertRaises(expected, mail._get_imap)
#
#    def test_imap_success(self):
#        """Test imap connection success."""
#        mail = Mail(self.gmail_server,
#                    self.empty_address,
#                    self.empty_password)
#        try:
#            mail._get_imap()
#        except Exception as e:
#            self.fail(e)
#
#    def test_imap_unknown(self):
#        """Test imap with an unknown address."""
#        mail = Mail(self.fake_server,
#                    self.empty_address,
#                    self.empty_password)
#        expected = Mail.ServerUnknownError
#        self.assertRaises(expected, mail._get_imap)
#
#    # LOGIN
#    def test_login_fail(self):
#        """Test login with wrong creditionals."""
#        mail = Mail(self.gmail_server, 
#                    self.fake_address,
#                    self.fake_password)
#        mail._get_imap()
#        expected = Mail.LoginFailure
#        self.assertRaises(expected, mail._login)
#
#    def test_login_empty_address(self):
#        """Test login with an empty address."""
#        mail = Mail(self.empty_server,
#                    self.empty_address,
#                    self.fake_password)
#        expected = Mail.EmptyAddress
#        self.assertRaises(expected, mail._login)
#
#    def test_login_empty_password(self):
#        """Test login with a empty password."""
#        mail = Mail(self.empty_server,
#                    self.fake_address,
#                    self.empty_password)
#        expected = Mail.EmptyPassword
#        self.assertRaises(expected, mail._login)
#
#    def test_login_config(self):
#        """Test login with config creditials and should succeed if correct."""
#        server, address, password, mailbox = self._get_config_creditials()
#        mail = Mail(server, address, password)
#        try:
#            mail._get_imap()
#            mail._login()
#        except Exception as e:
#            self.fail("Unexpected exception." + str(e))
#
#    # MAILBOX SELECTION
#    def test_mailbox_failure(self):
#        """Test mailbox selection with a fake mailbox."""
#        server, address, password, mailbox = self._get_config_creditials()
#        mailbox = self.fake_mailbox
#        mail = Mail(server, address, password, mailbox)
#        try:
#            mail._get_imap()
#            mail._login()
#        except Exception as e:
#            self.fail("Setup failed before test with unexpected exception." + str(e))
#        expected = Mail.MailboxSelectionError
#        self.assertRaises(expected, mail._select_mailbox)
#
#    def test_mailbox_success(self):
#        """Test mailbox selection success with default inbox."""
#        server, address, password, mailbox = self._get_config_creditials()
#        mailbox = 'inbox'
#        mail = Mail(server, address, password, mailbox)
#        try:
#            mail._get_imap()
#            mail._login()
#        except Exception as e:
#            self.fail("Setup failed before test with unexpected exception." + str(e))
#        try:    
#            mail._select_mailbox()
#        except Exception as e:
#            self.fail("Unexpected exception. " + str(e))
#
#    def test_mailbox_config(self):
#        """Test mailbox selection success with config mailbox."""
#        server, address, password, mailbox = self._get_config_creditials()
#        mail = Mail(server, address, password, mailbox)
#        try:
#            mail._get_imap()
#            mail._login()
#        except Exception as e:
#            self.fail("Setup failed before test with unexpected exception." + str(e))
#        try:    
#            mail._select_mailbox()
#        except Exception as e:
#            self.fail("Unexpected exception. " + str(e))
#
#    # MESSAGES
#    def test_markup_strip(self):
#        mail = Mail(self.empty_server, 
#                    self.empty_address,
#                    self.empty_password)
#        teststring = "<P>This is a test string.=0AA &amp; B.</P>"
#        expected = "This is a test string. A & B."
#        actual = mail._strip_message_markup(teststring)
#        self.assertEqual(expected, actual)
#
#    # HELPER FUNCTIONS
#    def _get_config_creditials(self):
#        """Get server, address, and password creditials from config file.
#           Using this instead of setup since not needed each time."""
#        if not self.config_isread:
#            try:
#                config = Config()
#                config.read()
#                self.config_server = config.server
#                self.config_address = config.address
#                self.config_password = config.password
#                self.config_mailbox = config.mailbox
#                self.config_isread = True
#            except Exception as e:
#                logger.error("Config.cfg was not found for intergation test.")
#                self.fail(e)
#        return self.config_server, self.config_address, self.config_password, self.config_mailbox


if __name__ == '__main__':
    unittest.main()

