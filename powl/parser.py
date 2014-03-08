"""Provides classes to parse messages and to parse for action data."""
import re
from powl import actiontype
from powl import actiondata


class Parser(object):
    """
    Provides methods to parse a string into a desired data structure.
    """

    def parse(self, string):
        """
        Parse a string into a desired data structure.

        Parameters
        ----------
        string : str
            String to parse.
        """
        pass


class BodyCompositionDataParser(Parser):
    """
    Parses a formatted string containing body composition data.
    """

    _TOKEN_FLAG = '-'
    _TOKEN_MASS = '^m'
    _TOKEN_FAT_PERCENTAGE = '^f'

    def parse(self, string):
        """
        Parse a formatted string into a BodyCompositionData object.

        Parameters
        ----------
        string : str
            String to parse.

        Returns
        -------
        powl.actiondata.BodyCompositionData
            Contains data to perform a body composition action.

        Raises
        ------
        ValueError
            If mass or fat percentage is not a float.
            If a value for BodyCompositionData is missing.
        """
        data = actiondata.BodyCompositionData()
        params = re.split(self._TOKEN_FLAG, string)

        for param in params:
            if re.match(self._TOKEN_MASS, param):
                data.mass = re.sub(self._TOKEN_MASS, '', param)
                data.mass = data.mass.strip()
            elif re.match(self._TOKEN_FAT, param):
                data.fat_percentage = re.sub(self._TOKEN_FAT, '', param)
                data.fat_percentage = data.fat_percentage.strip()

        if not data.mass:
            raise ValueError("Mass was not parsed")
        if not data.fat:
            raise ValueError("Fat was not parsed")

        try:
            float(data.mass)
        except ValueError:
            raise ValueError("Mass is not a number")
        try:
            float(data.fat_percentage)
        except ValueError:
            raise ValueError("Fat percentage is not a number")

        return data


class MessageParser(Parser):
    """
    Parses a formatted message containing an action and its data.
    """

    _DELIMITER = ' '

    def parse(self, string):
        """
        Parse a message into an action and its data string.

        Parameters
        ----------
        message : str
            Message to parse.

        Returns
        -------
        tuple of powl.actiontype and string
            The action type and the string containing data for the action.

        Raises
        ------
        ValueError
            If a valid action was not parsed.
        """
        action_key, data = message.split(self._DELIMITER, 1)

        try:
            action_type = actiontype.ACTION_MAP[action_key]
        except KeyError:
            raise KeyError("action key ({0}) is invalid".format(action_key))
        else:
            return action_type, data


class TransactionDataParser(Parser):
    """
    Parses a formatted string containing accounting data.
    """

    _TOKEN_FLAG = '-'
    _TOKEN_DEBIT = '^d'
    _TOKEN_CREDIT = '^c'
    _TOKEN_AMOUNT = '^a'
    _TOKEN_MEMO = '^m'

    def parse(self, string):
        """
        Parse a formatted string into a TransactionData object.

        Parameters
        ----------
        string : str
            String to parse.

        Returns
        -------
        powl.actiondata.TransactionData
            Contains data to perform a transaction action.

        Raises
        ------
        ValueError
            If amount is not a float.
            If a value for TransactionData is missing.
        """
        data = actiondata.AccountingData()
        params = re.split(self._TOKEN_FLAG, string)

        for param in params:
            if re.match(self._ACCOUNTING_TOKEN_DEBIT, param):
                data.debit = re.sub(self._ACCOUNTING_TOKEN_DEBIT, '', param)
                data.debit = data.debit.strip()
            elif re.match(self._ACCOUNTING_TOKEN_CREDIT, param):
                data.credit = re.sub(self._ACCOUNTING_TOKEN_CREDIT, '', param)
                data.credit = credit.strip()
            elif re.match(self._ACCOUNTING_TOKEN_AMOUNT, param):
                data.amount = re.sub(self._ACCOUNTING_TOKEN_AMOUNT, '', param)
                data.amount = amount.strip()
            elif re.match(self._ACCOUNTING_TOKEN_MEMO, param):
                data.memo = re.sub(self._ACCOUNTING_TOKEN_MEMO, '', param)
                data.memo = memo.replace("\"", '')
                data.memo = memo.strip()

        if not data.debit:
            raise ValueError("debit was not parsed")
        if not data.credit:
            raise ValueError("credit was not parsed")
        if not data.amount:
            raise ValueError("amount was not parsed")
        if not data.memo:
            raise ValueError("memo was not parsed")

        try:
            float(data.amount)
        except ValueError:
            raise ValueError("amount is not a number")

        return data

