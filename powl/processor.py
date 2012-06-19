#!/usr/bin/env python
"""Parse actions and processing for simpler actions."""
import re
from powl.actions import Actions

class MessageParser:

    def parse_message(self, message):
        """Parse a message and determine its specified action."""
        raw_action, data = message.split(' ', 1)
        if raw_action in Actions.actionable_list:
            action = raw_action
        else:
            action = Actions.nomatch
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

    def parse_bodycomposition(self, data):
        """Parse a body composition data into mass and body fat percentage."""
        mass = ''
        fat = ''
        params = re.split('-', data)
        for param in params:
            if re.match('^m', param):
                mass = re.sub('^m', '', param)
            elif re.match('^f', param):
                fat = re.sub('^f', '', param)
        mass = mass.strip()
        fat = fat.strip()
        return mass, fat

