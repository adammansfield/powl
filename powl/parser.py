#!/usr/bin/env python
"""Perform actions with given data."""
import re
from powl.actiontypes import ActionTypes

class Parser:

    def parse_message(self, message):
        """Parse a message and determine its specified action."""
        raw_action, data = message.split(' ', 1)
        if raw_action in ActionTypes.actionable:
            action = raw_action
        else:
            action = ActionTypes.nomatch
            data = message
        return action, data

    def parse_transaction(self, data):
        """Parse a transaction data into debit, credit, amount and memo."""
        debit = ''
        credit = ''
        amount = ''
        memo = ''
        params = re.split('-', data)
        for param in params:
            if re.match('^d', param):
                debit = re.sub('^d', '', param)
            elif re.match('^c', param):
                credit = re.sub('^c', '', param)
            elif re.match('^a', param):
                amount = re.sub('^a', '', param)
            elif re.match('^m', param):
                memo = re.sub('^m', '', param)
                memo = memo.replace("\"", '')
        debit = debit.strip()
        credit = credit.strip()
        amount = amount.strip()
        memo = memo.strip()
        return debit, credit, amount, memo

