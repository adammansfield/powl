#!/usr/bin/env python
"""Send and receive emails."""
import email
import errno
import imaplib
import socket
import sys

from powl import exception


class Mail(object):
    pass


class ImapMail(Mail):

    def __init__(self):
        # TODO: move to ImapMail.
        socket.setdefaulttimeout(self._TIMEOUT)


class Retriever(object):
    pass


class MailRetriever(Retriever):
    """
    Provides methods for retrieving a list of actions from a mailbox.
    """

    _ERROR_EMPTY_ADDRESS = "Empty email address."
    _ERROR_EMPTY_PASSWORD = "Empty email password."
    _ERROR_EMPTY_SERVER = "Empty server address."
    _ERROR_SERVER_NOT_FOUND = "{0} not found"
    _ERROR_TIMEOUT = "{0} has timed out"

    _MESSAGE_PART = '(RFC822)'
    _TIMEOUT = 5

    def __init__(self, mail, server, address, password, mailbox="inbox"):
        """
        Parameters
        ----------
        mail : powl.actionretriever.Mail
            Interface to the mail server.
        server : str
            IP address of the mail server.
        address : str
            Email address.
        password : str
            Email password.
        mailbox : str
            Default is "inbox".
        """
        self._server = server
        self._address = address
        self._password = password
        self._mailbox = mailbox

        if not self._server:
            msg = self._ERROR_EMPTY_SERVER
            err = exception.create(ValueError, msg)
            raise err

        if not self._address:
            msg = self._ERROR_EMPTY_ADDRESS
            err = exception.create(ValueError, msg)
            raise err

        if not self._password:
            msg = self._ERROR_EMPTY_PASSWORD
            err = exception.create(ValueError, msg)
            raise err

    # FETCHING
    def get_mail_list(self):
        """Get a list of tuples of unread email messages and their dates."""
        id_list = self._get_email_ids()
        mail_list = self._fetch_emails(id_list)
        message_list = self._parse_email_messages(mail_list)
        date_list = self._parse_email_date(mail_list)
        combined_list = zip(message_list, date_list)
        return combined_list

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
            result, response = self._imap.fetch(email_id, self._MESSAGE_PART)
            mail_data = response[0]
            mail_string = mail_data[1]
            mail_object = email.message_from_string(mail_string)
            mail_list.append(mail_object)
        return mail_list

    # PARSING
    def _parse_email_messages(self, mail_list):
        """Return a list of messages parsed from the mail list."""
        message_list = []
        for mail in mail_list:
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload()
                    message = self._strip_message_markup(body).strip()
                    logger.debug('EMAIL   %s', message)
                    message_list.append(message)
        return message_list

    def _parse_email_date(self, mail_list):
        """Return a list of dates parsed from the mail list."""
        date_list = []
        for mail in mail_list:
            date = email.utils.parsedate(mail['Date'])
            date_list.append(date)
        return date_list

    def _strip_message_markup(self, message):
        """Return message striped of markup."""
        retval = message
        retval = retval.replace('<P>','')
        retval = retval.replace('</P>','')
        retval = retval.replace('=0A',' ')
        retval = retval.replace('&amp;','&')
        return retval

    # IMAP SETUP
    def setup(self):
        """Get imap server, login and select mailbox."""
        try:
            self._get_imap()
            self._login()
            self._select_mailbox()
        except Mail.MailError as e:
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
        result, response = self._imap.select(self._mailbox)
        if "NO" in response:
            message = self._mailbox + " is not a valid mailbox."
            raise self.MailboxSelectionError(message)

