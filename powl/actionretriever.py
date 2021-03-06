"""Send and receive emails."""
import email
from powl import exception


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

    _MESSAGE_PART = '(RFC822)'

    def __init__(self, mail, server, user, password):
        """
        Parameters
        ----------
        mail : powl.mail.Mail
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

    def _convert_message_to_action_item(self, message):
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

