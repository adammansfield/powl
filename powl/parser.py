"""Provides classes to parse messages and to parse for action data."""
import re
from powl import actiontype
from powl import actiondata
from powl import exception


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
        except KeyError as err:
            msg = "action key ({0}) is unknown".format(action_key)
            exception.add_message(err, msg)
            raise
        else:
            return action_type, data


class BodyCompositionDataFlagParser(Parser):
    """
    Parses a string containing body composition data based on flags.
    """

    _TOKEN_FLAG = '-'
    _TOKEN_MASS = '^m'
    _TOKEN_FAT = '^f'

    def parse(self, string):
        """
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
        params = string.split(self._TOKEN_FLAG)

        for param in params:
            if re.match(self._TOKEN_MASS, param):
                data.mass = re.sub(self._TOKEN_MASS, '', param)
                data.mass = data.mass.strip()
            elif re.match(self._TOKEN_FAT, param):
                data.fat_percentage = re.sub(self._TOKEN_FAT, '', param)
                data.fat_percentage = data.fat_percentage.strip()

        if not data.mass:
            msg = "mass was not parsed from ({0})".format(string)
            err = exception.create(ValueError, msg)
            raise err

        if not data.fat_percentage:
            msg =("fat percentage was not parsed " +
                  "from ({0})".format(string))
            err = exception.create(ValueError, msg)
            raise err

        try:
            float(data.mass)
        except ValueError as err:
            msg = "mass ({0}) is not a number".format(data.mass)
            exception.add_message(err, msg)
            raise

        try:
            float(data.fat_percentage)
        except ValueError as err:
            msg = ("fat percentage ({0}) ".format(data.fat_percentage) +
                   "is not a number")
            exception.add_message(err, msg)
            raise

        return data


class BodyCompositionDataPositionalParser(Parser):
    """
    Parses a string containing body composition data based on position.
    """

    _DELIMITER = ' '
    _POSITION_MASS = 0
    _POSITION_FAT = 1
    _NUM_PARAMS = 2
    _MAX_SPLITS = _NUM_PARAMS - 1

    def parse(self, string):
        """
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
        params = re.split(self._DELIMITER, string, self._MAX_SPLITS)

        if len(params) < self._NUM_PARAMS:
            msg = "not enough arguments from ({0})".format(string)
            err = exception.create(ValueError, msg)
            raise err

        mass = params[self._POSITION_MASS]
        fat_percentage = params[self._POSITION_FAT]

        try:
            data.mass = float(mass)
        except ValueError as err:
            msg = "mass ({0}) is not a number".format(mass)
            exception.add_message(err, msg)
            raise

        try:
            data.fat_percentage = float(fat_percentage)
        except ValueError as err:
            msg =("fat percentage ({0}) ".format(fat_percentage) +
                  "is not a number")
            exception.add_message(err, msg)
            raise

        return data


class TransactionDataFlagParser(Parser):
    """
    Parses a formatted string containing accounting data based on flag
    arguments.
    """

    _TOKEN_FLAG = '-'
    _TOKEN_DEBIT = '^d'
    _TOKEN_CREDIT = '^c'
    _TOKEN_AMOUNT = '^a'
    _TOKEN_MEMO = '^m'

    def parse(self, string):
        """
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
        params = string.split(self._TOKEN_FLAG)

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
            msg = "debit is missing from ({0})".format(string)
            err = exception.create(ValueError, msg)
            raise err

        if not data.credit:
            msg = "credit is missing from ({0})".format(string)
            err = exception.create(ValueError, msg)
            raise err

        if not data.amount:
            msg = "amount is missing from ({0})".format(string)
            err = exception.create(ValueError, msg)
            raise err

        if not data.memo:
            msg = "memo is missing from ({0})".format(string)
            err = exception.create(ValueError, msg)
            raise err

        try:
            float(data.amount)
        except ValueError as err:
            message = "amount ({0}) is not a number".format(data.amount)
            exception.add_message(err, message)
            raise

        return data


class TransactionDataPositionalParser(Parser):
    """
    Parses a formatted string containing accounting data based on
    positional arguments.
    """

    _DELIMITER = ' '
    _POSITION_AMOUNT = 0
    _POSITION_DEBIT = 1
    _POSITION_CREDIT = 2
    _POSITION_MEMO = 3
    _NUM_PARAMS = 4
    _MAX_SPLITS = _NUM_PARAMS - 1

    def parse(self, string):
        """
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
        params = string.split(self._DELIMITER, self._MAX_SPLITS)

        if len(params) < self._NUM_PARAMS:
            msg = "not enough arguments from ({0})".format(string)
            err = exception.create(ValueError, msg)
            raise err

        data.debit = params[self._POSITION_DEBIT]
        data.credit = params[self._POSITION_CREDIT]
        data.amount = params[self._POSITION_AMOUNT]
        data.memo = params[self._POSITION_MEMO]

        try:
            float(data.amount)
        except ValueError:
            msg = "amount ({0}) is not a number".format(data.amount)
            err = exception.create(ValueError, msg)
            raise err

        return data

