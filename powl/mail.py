#!/usr/bin/env python
"""To get email from a mailbox and to send emails."""
#import ConfigParser
#import email
import errno
import imaplib
#import logging
#import optparse
#import os
#import re
#import shutil
import socket
import sys
#import textwrap
#import time
import powl.logger as logger
#import powl.output as output
#from powl.config import Config
#from powl.processors.transaction import Transaction



class Mail:
    """To get email from a mailbox and to send emails."""

    # CONSTANTS
    _message_part = '(RFC822)'
    _timeout = 5

    # EXCEPTIONS
    class MailError(Exception): pass
    class EmptyServer(MailError): pass
    class EmptyAddress(MailError): pass
    class EmptyPassword(MailError): pass
    class ServerUnknownError(MailError): pass
    class ServerTimedOutError(MailError): pass
    class ServerUnreachableError(MailError): pass
    class LoginFailure(MailError): pass
    class MailboxSelectionError(MailError): pass


    # FETCHING
    def process(self):
        """Parse through an inbox of emails."""
        search_response, email_ids = self.imap.search(None, "(Unseen)")
        logger.info("PROCESSING INBOX")
        for email_id in email_ids[0].split():
            fetch_response, data = self.imap.fetch(email_id, "(RFC822)")
            mail = email.message_from_string(data[0][1])
            date = email.utils.parsedate(mail['Date'])
            # done up till here
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload()
                    message = self.strip_message_markup(body)
                    logger.debug('EMAIL   %s', message.strip())
                    self.parse_message(message, date)

    def get_messages(self):
        """Get a list of tuples of unread email messages and their dates."""
        id_list = self._get_email_id_list()
        mail_list = self._fetch_emails(id_list)
        message_list = self._parse_email_message(mail_list)
        date_list = self._parse_email_date(mail_list)

    def _get_email_ids(self, charset=None, criteria="(Unseen)"):
        """Get a list of email ids for messages."""
        result, response = self._imap.search(charset, criteria)
        id_string = response[0]
        id_list = id_string.split()
        return id_list

    def _fetch_emails(self, id_list):
        """Return email objects fetched using the id list parameter."""
        mail_list = []
        for email_id in id_list:
            result, response = self._imap.fetch(email_id, self._message_part)
            mail_data = response[0]
            mail_string = mail_data[1]
            mail_object = email.message_from_string(mail_string)
            mail_list.append(mail_object)
        return mail_list

    def _parse_email_messages(self, mail_list):
        """Return a list of messages parsed from the mail list."""
        message_list = []
        for mail in mail_list:
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload()
                    message = self._strip_message_markup(body)
                    message_list.append(message)
        return message_list

    def _parse_email_date(self, mail_list):
        """Return a list of dates parsed from the mail list."""
        date_list = []
        for mail in mail_list:
            date = email.utils.parsedate(mail['Date'])
            date_list.append(date)
        return date_list

    # MARKUP CLEANUP
    def _strip_message_markup(self, message):
        """Return message striped of markup."""
        retval = message
        retval = retval.replace('<P>','')
        retval = retval.replace('</P>','')
        retval = retval.replace('=0A',' ')
        retval = retval.replace('&amp;','&')
        return retval

    # SETUP
    def setup(self):
        """Get imap server, login and select mailbox."""
        try:
            self._get_imap()
            self._login()
        except MailError as e:
            logger.error(e)
            sys.exit(e)

    def _get_imap(self):
        """Attempt to get imap object."""
        if not self._server:
            raise self.EmptyServer("Imap server has not been set.")
        else:
            try:
                self._imap = imaplib.IMAP4_SSL(self._server)
            except socket.gaierror as (code, message):
                if code == socket.EAI_NONAME:
                    message = self._server + " not found."
                    raise self.ServerUnknownError(message)
            except socket.error as (code, message):
                if code == errno.ENETUNREACH:
                    message = self._server + " not found."
                    raise self.ServerUnreachableError(message)
            except socket.timeout:
                message = self._server + " has timed out."
                raise self.ServerTimedOutError(message)

    def _login(self):
        """Login to imap server and select mailbox."""
        if not self._address:
            raise self.EmptyAddress("Empty Address.")
        elif not self._password:
            raise self.EmptyPassword("Empty Password.")
        else:
            try:    
                self._imap.login(self._address, self._password)
            except imaplib.IMAP4.error as e:
                if "Invalid credentials" in str(e):
                    message = (
                        "{0} {1} are invalid creditials.".format(self._address,
                                                                 self._password)
                    )
                    raise self.LoginFailure(message)

    def _select_mailbox(self):
        """Select a mailbox from the imap object."""
        status, result = self._imap.select(self._mailbox)
        if "NO" in status:
            message = self._mailbox + " is not a valid mailbox."
            raise self.MailboxSelectionError(message)

    # INTIALIZATION
    def __init__(self, server, address, password, mailbox='inbox'):
        self._server = server
        self._address = address
        self._password = password
        self._mailbox = mailbox
        socket.setdefaulttimeout(self._timeout)
