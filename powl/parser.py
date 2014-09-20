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


class ActionItemParser(Parser):
    """
    Parses an item containing an action and its data.
    """

    _DELIMITER = ' '

    def parse(self, item):
        """
        Parse an action item into an action type and its data.

        Parameters
        ----------
        item : str
            Item to parse.

        Returns
        -------
        tuple of powl.actiontype and str
            The action type and a string containing data for the action.

        Raises
        ------
        KeyError
            If the action_key is not in the action map.
        ValueError
            If a valid action was not parsed.
        """
        action_key, data = item.split(self._DELIMITER, 1)

        try:
            action_type = actiontype.ACTION_MAP[action_key]
        except KeyError:
            raise KeyError("action key ({0}) is invalid".format(action_key))
        else:
            return action_type, data


class BodyCompositionDataFlagParser(Parser):
    """
    Parses a string containing body composition data.
    """

    _TOKEN_FLAG = '-'
    _TOKEN_MASS = '^m'
    _TOKEN_FAT = '^f'

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
            raise ValueError("mass was not parsed from ({0})".format(string))
        if not data.fat_percentage:
            raise ValueError("fat percentage was not parsed from "
                             "({0})".format(string))

        try:
            float(data.mass)
        except ValueError:
            raise ValueError("mass is not a number ({0})".format(data.mass))
        try:
            float(data.fat_percentage)
        except ValueError:
            raise ValueError("fat percentage is not a number "
                             "({0})".format(data.fat_percentage))
        return data


class TransactionDataFlagParser(Parser):
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
        data = actiondata.TransactionData()
        params = re.split(self._TOKEN_FLAG, string)

        for param in params:
            if re.match(self._TOKEN_DEBIT, param):
                data.debit = re.sub(self._TOKEN_DEBIT, '', param)
                data.debit = data.debit.strip()
            elif re.match(self._TOKEN_CREDIT, param):
                data.credit = re.sub(self._TOKEN_CREDIT, '', param)
                data.credit = data.credit.strip()
            elif re.match(self._TOKEN_AMOUNT, param):
                data.amount = re.sub(self._TOKEN_AMOUNT, '', param)
                data.amount = data.amount.strip()
            elif re.match(self._TOKEN_MEMO, param):
                data.memo = re.sub(self._TOKEN_MEMO, '', param)
                data.memo = data.memo.replace("\"", '')
                data.memo = data.memo.strip()

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

