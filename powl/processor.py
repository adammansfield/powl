#!/usr/bin/env python
"""Parse actions and processing for simpler actions."""
import re

class Processor:

    action_bodycomposition = 'bodycomposition'
    action_event = 'event'
    action_note = 'note'
    action_todo = 'todo'
    action_transaction = 'transaction'
    _action_list = [
        action_bodycomposition,
        action_event,
        action_note,
        action_todo,
        action_transaction
    ]
    action_nomatch = 'nomatch'

    def parse_message(self, message):
        """Parse a message and determine its specified action."""
        raw_action, data = message.split(' ', 1)
        if raw_action in self._action_list:
            action = raw_action
        else:
            action = self.action_nomatch
            data = message
        return action, data

    def parse_transaction(self, data):
        """Parse a transaction data into debit, credit, amount and memo."""
        params = re.split('-', data)
        for param in params:
            param = param.strip()
            if re.match('^d', param):
                debit = param.replace('d ','')
            elif re.match('c', param):
                credit = param.replace('c ','')
            elif re.match('a', param):
                amount = param.replace('a ','')
            elif re.match('m', param):
                memo = param.replace('m ','')
                memo = memo.replace("\"", '')
                memo = memo.strip()
        return debit, credit, amount, memo

