#!/usr/bin/env python
"""Send and receive emails."""
import email
import errno
import imaplib
import socket
import sys
from powl import exception


class MailMessage(object):
    """
    Contains data about an email message.

    Attributes
    ----------
    body : str
    date : time.struct_time
    """

    def __init__(self):
        self.body = None
        self.date = None


class Mail(object):

    _ERROR_CONNECT_UNKNOWN = "unknown connect error to {0}"
    _ERROR_INVALID_CREDENTIALS = "invalid email credentials"
    _ERROR_NOT_CONNECTED = "not connected to mail server"
    _ERROR_NOT_LOGGED_IN = "not logged in to mail server"
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

    def get_messages(self):
        """
        Returns
        -------
        list of powl.actionretriver.MailMessage
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


class ImapMail(Mail):

    _ERROR_INVALID_MAILBOX = "{0} is an invalid mailbox folder"

    def __init__(self, mailbox="inbox", timeout=5, charset = None,
                 criteria="(Unseen)"):
        """
        Parameters
        ----------
        mailbox : str
            Default is "inbox".
        timeout : int
            Timeout for connection to IMAP server.
        charset : str
            Charset used for IMAP4.search used to retrive mail ids.
        criteria : str
            Criteria used for IMAP4.search used to retrieve mail ids.
        """
        self._mailbox = mailbox
        self._timeout = timeout
        self._charset = charset
        self._criteria = criteria

        self._imap = None
        self._logged_in = False
        socket.setdefaulttimeout(self._timeout)

    def _fetch_emails(self, email_id_list):
        """
        Return all email objects fetched using the ids from the id list.
        """
        email_list = []
        for email_id in email_id_list:
            result, response = self._imap.fetch(email_id, self._MESSAGE_PART)
            email_string = response[0][1]
            email_object = email.message_from_string(email_string)
            email_list.append(email_object)
        return email_list

    def _get_message_id_list(self):
        """
        Returns a list of email message ids.
        """
        result, response = self._imap.search(self._charset, self._criteria)
        id_list_string = response[0]
        id_list = id_list_string.split()
        return id_list

    def _parse_email_body(self, email_object):
        """
        Return the body of the given email.
        """
        body = ""
        for part in email_object.walk():
            if part.get_content_type() == 'text/html':
                body = part.get_payload()
                break
        return self._strip_markup(body)

    def _parse_email_date(self, email_object):
        """
        Return the date of the given emai.
        """
        date_string = email_object["Date"]
        date = email.utils.parsedate(date_string)
        return date

    def _strip_markup(self, string):
        """
        Return message stripped of markup.
        """
        retval = string.replace('<P>','')
        retval = retval.replace('</P>','')
        retval = retval.replace('=0A',' ')
        retval = retval.replace('&amp;','&')
        retval = retval.strip()
        return retval

    def _select_mailbox(self):
        """
        Select a mailbox folder.
        """
        result, response = self._imap.select(self._mailbox)
        if result == "NO":
            msg = self._ERROR_INVALID_MAILBOX.format(self._mailbox)
            err = exception.create(ValueError, msg)
            raise err

    # Mail methods.
    def connect(self, server):
        try:
            self._imap = imaplib.IMAP4_SSL(server)
        except socket.timeout as err:
            msg = self._ERROR_TIMEOUT.format(server)
            exception.add_message(err, msg)
            raise
        except IOError as err:
            if err.errno == socket.EAI_NONAME:
                msg = self._ERROR_SERVER_NOT_FOUND.format(server)
            elif err.errno == socket.errno.ENETUNREACH:
                msg = self._ERROR_SERVER_NOT_FOUND.format(server)
            else:
                msg = self._ERROR_CONNECT_UNKNOWN.format(server)
            exception.add_message(err, msg)
            raise

    def get_messages(self):
        if not self._imap:
            msg = self._ERROR_NOT_CONNECTED
            err = exception.create(ValueError, msg)
            raise err

        if not self._logged_in:
            msg = self._ERROR_NOT_LOGGED_IN
            err = exception.create(ValueError, msg)
            raise err

        id_list = self._get_message_id_list()
        email_list = self._fetch_emails(id_list)

        messages = []
        for email_object in email_list:
            message = Message()
            message.body = self._parse_email_body(email_object)
            message.date = self._parse_email_date(email_object)
            messages.append(message)

        return messages

    def login(self, user, password):
        if not self._imap:
            msg = self._ERROR_NOT_CONNECTED
            err = exception.create(ValueError, msg)
            raise err

        try:
            self._imap.login(user, password)
        except imaplib.IMAP4.error as err:
            if ("Invalid credentials" in str(err) or
                    "AUTHENTICATIONFAILED" in str(err)):
                msg = self._ERROR_INVALID_CREDENTIALS
                exception.add_message(err, msg)
            raise

        self._select_mailbox()
        self._logged_in = True


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

    def _convert_message_to_action_item(self, message)
        """
        Return an ActionItem from a Message.
        """
        action_item = ActionItem()
        action_item.action = message.body
        action_item.date = message.date
        return action_item

    def get_action_items(self):
        """
        Return a list of action items retrieved from a mail box.
        """
        self._mail.connect(self._server)
        self._mail.login(self._user, self._password)
        messages = self._mail.get_messages()

        action_items = []
        for message in messages:
            action_item = self._convert_message_to_action_item(message)
            action_items.append(action_item)
        return action_items

