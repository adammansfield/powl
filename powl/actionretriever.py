#!/usr/bin/env python
"""Send and receive emails."""
import email
import errno
import imaplib
import socket
import sys
from powl import exception


class Mail(object):

    _ERROR_CONNECT_UNKNOWN = "unknown connect error to {0}"
    _ERROR_INVALID_CREDENTIALS = "invalid email credentials"
    _ERROR_NOT_CONNECTED = "not connected to mail server"
    _ERROR_SERVER_NOT_FOUND = "{0} not found"
    _ERROR_TIMEOUT = "{0} has timed out"

    def connect(self, server):
        """
        Parameters
        ----------
        server : str
            URL or ip address of the mail server.
        """
        raise NotImplementedError()

    def login(self, user, password):
        """
        Paramaters
        ----------
        user : str
            User email address.
        password : str
            Password for email address.
        """
        raise NotImplementedError()

    def get_message_id_list(self):
        """
        Returns
        -------
        list of str
            IDs that can be used to get the messages.
        """
        raise NotImplementedError()

    def get_message_and_date(self, message_id):
        """
        Parameters
        ----------
        message_id : str

        Returns
        -------
        tuple of str, time.struct_time
            The str is the body of the message.
            The time.struct_time is the date of the message.
        """
        raise NotImplementedError()


class ImapMail(Mail):

    _ERROR_INVALID_MAILBOX = "{0} is an invalid mailbox folder"

    def __init__(self, mailbox="inbox", timeout=5):
        """
        Parameters
        ----------
        mailbox : str
            Default is "inbox".
        """
        self._mailbox = mailbox
        self._timeout = timeout

        self._imap = None
        socket.setdefaulttimeout(self._timeout)

    def connect(self, server):
        try:
            self._imap = imaplib.IMAP4_SSL(server)
        except socket.timeout as err:
            msg = self._ERROR_TIMEOUT.format(server)
            exception.add_message(err, msg)
            raise
        except IOError as err:
            if err.errno == socket.EAI_NONAME:
                msg = self._ERROR_SERVER_NOT_FOUND.format(self._server)
            elif err.errno == socket.ENETUNREACH:
                msg = self._ERROR_SERVER_NOT_FOUND.format(self._server)
            else:
                msg = self._ERROR_CONNECT_UNKNOWN.format(self._server)
            exception.add_message(err, msg)
            raise

    def login(self, user, password):
        if not self._imap:
            msg = self._ERROR_NOT_CONNECTED
            err = exception.create(ValueError, msg)
            raise err
        try:
            self._imap.login(user, password)
        except imaplib.IMAP4.error as err:
            if "Invalid credentials" in str(e):
                msg = self._ERROR_INVALID_CREDENTIAL
                exception.add_message(err, msg)
                raise
        self._select_mailbox()

    def get_message_id_list(self):
        if not self._imap:
            msg = self._ERROR_NOT_CONNECTED
            err = exception.create(ValueError, msg)
            raise err

    def _select_mailbox(self):
        """
        Select a mailbox folder.
        """
        result, response = self._imap.select(self._mailbox)
        if result == "NO":
            msg = self._ERROR_INVALID_MAILBOX.format(self._mailbox)
            err = exception.create(ValueError, msg)
            raise err


class ActionItemRetriever(object):
    """
    Provides methods for retrieving a list of action items.
    """

    def get_action_items(self):
        """
        Get and return a list of action items.

        Returns
        -------
        list of (str, time.struct_time)
        """
        pass


class MailRetriever(ActionItemRetriever):
    """
    Provides methods for retrieving a list of actions from a mailbox.
    """

    _ERROR_EMPTY_USER = "Empty email address."
    _ERROR_EMPTY_PASSWORD = "Empty email password."
    _ERROR_EMPTY_SERVER = "Empty server address."

    _MESSAGE_PART = '(RFC822)'

    def __init__(self, mail, server, user, password):
        """
        Parameters
        ----------
        mail : powl.actionretriever.Mail
            Interface to the mail server.
        server : str
            IP address of the mail server.
        user : str
            Email address.
        password : str
            Email password.
        """
        self._mail = mail
        self._server = server
        self._user = user
        self._password = password

        if not self._server:
            msg = self._ERROR_EMPTY_SERVER
            err = exception.create(ValueError, msg)
            raise err

        if not self._user:
            msg = self._ERROR_EMPTY_USER
            err = exception.create(ValueError, msg)
            raise err

        if not self._password:
            msg = self._ERROR_EMPTY_PASSWORD
            err = exception.create(ValueError, msg)
            raise err

    def get_action_items(self):
        """
        Return a list of action items retrieved from a mail box.
        """
        try:
            self._mail.connect(self._server)
        except socket.timeout as err:
            msg = self._ERROR_TIMEOUT.format(self._server)
            exception.add_message(err, msg)
            raise
        except IOError as err:
            if err.errno == socket.EAI_NONAME:
                msg = self._ERROR_SERVER_NOT_FOUND.format(self._server)
            elif err.errno == socket.ENETUNREACH:
                msg = self._ERROR_SERVER_NOT_FOUND.format(self._server)
            else:
                msg = self._ERROR_CONNECT_UNKNOWN.format(self._server)
            exception.add_message(err, msg)
            raise

        self._mail.login(self._user, self._password)

        message_id_list = self._mail.get_message_id_list()

        for message_id in message_id_list:
            message = self._mail.get_message(message_id)



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

