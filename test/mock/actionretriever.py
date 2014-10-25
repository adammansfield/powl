"""Provides mock objects for powl.actionretriever."""
from powl import actionretriver

class MockMail(actionretriver.Mail):
    """
    Provides a mock object for powl.actionretriver.Mail.
    """

    def __init(self, server, user, password, messages):
        """
        Parameters
        ----------
        server : str
        user : str
        password : str
        messages
        """
        self._server = server
        self._user = user
        self._password = password
        self._message = messages
        self._connected = False

    # powl.actionretriever.Mail methods.
    def connect(self, server):
        pass

    def login(self, user, password):
        pass

    def get_message_id_list(self):
        pass

    def get_message_and_date(self, message_id):
        pass

