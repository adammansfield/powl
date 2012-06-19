#!/usr/bin/env python
"""Perform actions with given data."""
import os
import re
import powl.output as output

class Actions:
    """Contains definitions for possible actions."""
    nomatch = 'nomatch'
    bodycomposition = 'bodycomposition'
    event = 'event'
    note = 'note'
    todo = 'todo'
    transaction = 'transaction'
    actionable_list = [
        bodycomposition,
        event,
        note,
        todo,
        transaction
    ]


    # ACTIONS
    def do_action(self, message, date):
        """Determine and do the specified action."""
        action, data = self._parse_message(message)
        self._action_to_method_map[action](data, date)

    def _process_bodycomposition(self, data, date):
        pass

    def _process_event(self, data, date):
        pass

    def _process_note(self, data, date):
        # TODO: replace next two lines with data.py interface
        filepath = os.path.join(self._output_dir, 'miscellaneous.txt')
        data = data + os.linesep
        output.append(filename, data)

    def _process_nomatch(self, data, date):
        pass

    def _process_todo(self, data, date):
        pass

    def _process_transaction(self, data, date):
        """Separate transaction data to pass onto processing."""
        debit, credit, amount, memo = self._parse_transaction(data)
        filename, data = self._transaction.process(date, debit, credit, amount, memo)
        # TODO: replace next three lines with data.py interface
        if filename:
            filepath = os.path.join(self._transaction_dir, filename)
            output.append(filepath, data)

    # PARSING
    def _parse_message(self, message):
        """Parse a message and determine its specified action."""
        raw_action, data = message.split(' ', 1)
        if raw_action in Actions.actionable_list:
            action = raw_action
        else:
            action = Actions.nomatch
            data = message
        return action, data

    def _parse_transaction(self, data):
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

    def _parse_bodycomposition(self, data):
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

    # INITIALIZATION
    def __init__(self, mail, transaction_processor, output_dir, transaction_dir):
        self._mail = mail
        self._transaction = transaction_processor
        self._output_dir = output_dir   # TODO: abstract this to data.py
        self._transaction_dir = transaction_dir # TODO: abstract this to data.py
        self._action_to_method_map = {
            self.nomatch: self._process_nomatch,
            self.bodycomposition: self._process_bodycomposition,
            self.event: self._process_event,
            self.note: self._process_note,
            self.todo: self._process_todo,
            self.transaction: self._process_transaction
        }
