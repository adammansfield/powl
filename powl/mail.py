"""Provides methods for retrieving messages from mailboxes."""
import email
import imaplib
import socket
from powl import exception

class MessageHelper(object):
    """
    Provides methods for extracting data from email.message.Message.
    """

    def __init__(self, message):
        """
        Parameters
        ----------
        message : email.message.Message
        """
        self._message = message

    def _strip_markup(self, string):
        """
        Return string stripped of markup and surrounding whitespace.
        """
        retval = string.replace('<P>','')
        retval = retval.replace('</P>','')
        retval = retval.replace('=0A',' ')
        retval = retval.replace('&amp;','&')
        retval = retval.strip()
        return retval

    def get_body(self):
        """
        Return the body of the given email.

        Returns
        -------
        str
        """
        raw_body = ""
        for part in self._message.walk():
            if part.get_content_type() == 'text/plain':
                raw_body = part.get_payload()
        body = self._strip_markup(raw_body)
        return body

    def get_date(self):
        """
        Return the date of the given emai.

        Returns
        -------
        time.struct_time
        """
        date_string = self._message["Date"]
        date = email.utils.parsedate(date_string)
        return date


class Mail(object):
    """
    Provides methods for retrieving messages from mail servers.
    """

    _ERRMSG_CONNECT_UNKNOWN = "unknown connect error to {0}"
    _ERRMSG_INVALID_CREDENTIALS = "invalid email credentials"
    _ERRMSG_NOT_CONNECTED = "not connected to mail server"
    _ERRMSG_NOT_LOGGED_IN = "not logged in to mail server"
    _ERRMSG_SERVER_NOT_FOUND = "{0} not found"
    _ERRMSG_TIMEOUT = "{0} has timed out"

    def connect(self, server):
        """
        Establishes a connection to the mail server.

        Parameters
        ----------
        server : str
            URL or ip address of the mail server.
        """
        raise NotImplementedError()

    def get_messages(self):
        """
        Retrieves all unread mail messages.

        Returns
        -------
        list of email.message.Message
        """
        raise NotImplementedError()

    def login(self, user, password):
        """
        Log in to the mail server with the given username and password.

        Paramaters
        ----------
        user : str
            User email address.
        password : str
            Password for email address.
        """
        raise NotImplementedError()


class ImapMail(Mail):
    """
    Implements Mail using imaplib.IMAP4_SSL.
    """

    _ERRMSG_INVALID_MAILBOX = "{0} is an invalid mailbox folder"

    _MESSAGE_PART = "(RFC822)"

    def __init__(self, mailbox="inbox", timeout=5, charset=None,
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

    def _assert_connected(self):
        """
        Raise exception if not connected to IMAP server.
        """
        if not self._imap:
            msg = self._ERRMSG_NOT_CONNECTED
            err = exception.create(ValueError, msg)
            raise err

    def _assert_logged_in(self):
        """
        Raise exception if not logged in to IMAP server.
        """
        if not self._logged_in:
            msg = self._ERRMSG_NOT_LOGGED_IN
            err = exception.create(ValueError, msg)
            raise err

    def _get_message_ids(self):
        """
        Return a list of email message ids.
        """
        result, response = self._imap.search(self._charset, self._criteria)
        id_list_string = response[0]
        id_list = id_list_string.split()
        return id_list

    def _get_messages(self, message_ids):
        """
        Return all email.message.Message fetched using the given id list.
        """
        messages = []
        for message_id in message_ids:
            result, response = self._imap.fetch(message_id, self._MESSAGE_PART)
            message_string = response[0][1]
            message = email.message_from_string(message_string)
            messages.append(message)
        return messages

    def _select_mailbox(self):
        """
        Select a mailbox folder.
        """
        result, response = self._imap.select(self._mailbox)
        if result == "NO":
            msg = self._ERRMSG_INVALID_MAILBOX.format(self._mailbox)
            err = exception.create(ValueError, msg)
            raise err

    # powl.actionretriever.Mail methods.
    def connect(self, server):
        try:
            self._imap = imaplib.IMAP4_SSL(server)
        except socket.timeout as err:
            msg = self._ERRMSG_TIMEOUT.format(server)
            exception.add_message(err, msg)
            raise
        except IOError as err:
            if err.errno == socket.EAI_NONAME:
                msg = self._ERRMSG_SERVER_NOT_FOUND.format(server)
            elif err.errno == socket.errno.ENETUNREACH:
                msg = self._ERRMSG_SERVER_NOT_FOUND.format(server)
            else:
                msg = self._ERRMSG_CONNECT_UNKNOWN.format(server)
            exception.add_message(err, msg)
            raise

    def get_messages(self):
        self._assert_connected()
        self._assert_logged_in()

        message_ids = self._get_message_ids()
        messages = self._get_messages(message_ids)

        return messages

    def login(self, user, password):
        self._assert_connected()

        try:
            self._imap.login(user, password)
        except imaplib.IMAP4.error as err:
            if ("Invalid credentials" in str(err) or
                    "AUTHENTICATIONFAILED" in str(err)):
                msg = self._ERRMSG_INVALID_CREDENTIALS
                exception.add_message(err, msg)
            raise

        self._select_mailbox()
        self._logged_in = True

