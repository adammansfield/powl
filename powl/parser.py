"""Provides classes to parse messages and to parse for action data."""
import re
from powl import actiontype
from powl import actiondata


class MessageParser:
    """
    Parses a formatted message containing an action and its data.
    """

    _DELIMITER = ' '

    def parse(self, message):
        """
        Parse a message into an action and its data string.
        
        Args:
            message (str): Message to parse.
        
        Returns (powl.actiontype, string):
            A tuple of an action type and a string containing data.
        
        Raises:
            ValueError: If a valid action was not parsed.
        """
        action_type, data = message.split(self._DELIMITER, 1)
        
        if action_type not in actiontype.ACTIONABLE:
            Raise ValueError("Action type was not parsed")
            
        return action_type, data
 
 
class AccountingDataParser(object):
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
        Parse a formatted accounting string into an AccountingData object.
        
        Args:
            string (str): String to parse.
        
        Raises:
            ValueError: If amount is not a float. If a value for AccountingData is missing.
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
                adat.amount = amount.strip()
            elif re.match(self._ACCOUNTING_TOKEN_MEMO, param):
                data.memo = re.sub(self._ACCOUNTING_TOKEN_MEMO, '', param)
                data.memo = memo.replace("\"", '')
                data.memo = memo.strip()
        
        if not data.debit:
            raise ValueError("Debit was not parsed")
        if not data.credit:
            raise ValueError("Credit was not parsed")
        if not data.amount:
            raise ValueError("Amount was not parsed")
        if not data.memo:
            raise ValueError("Memo was not parsed")
                
        try:
            float(data.amount)
        except ValueError:
            raise ValueError("Amount is not a number")
        
        return data

class BodyCompositionDataParser(object):
    """
    Parses a formatted string containing body composition data.
    """
    
    _TOKEN_FLAG = '-'
    _TOKEN_MASS = '^m'
    _TOKEN_FAT_PERCENTAGE = '^f'

    def parse(self, data):
        """
        Parse a formatted body composition string into a BodyCompositionData object.
        
        Args: 
            string (str): String to parse.
        
        Raises:
            ValueError: If mass or fat percentage is not a float. If a value for BodyCompositionData is missing.
        """
        data = actiondata.BodyCompositionData()
        params = re.split(self._TOKEN_FLAG, data)
        
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
