#!/usr/bin/env python
"""Perform actions with given data."""
import os
import re
import powl.output as output
from powl.actiontypes import ActionTypes
from powl.parser import Parser

class Actions:

    # ACTIONS
    def do_action(self, action, data, date):
        """Determine and do the specified action."""
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
        debit, credit, amount, memo = self._parser.parse_transaction(data)
        filename, data = self._transaction.process(date, debit, credit, amount, memo)
        # TODO: replace next three lines with data.py interface
        if filename:
            filepath = os.path.join(self._transaction_dir, filename)
            output.append(filepath, data)


    # INITIALIZATION
    def __init__(self, mail, transaction_processor, output_dir, transaction_dir):
        self._mail = mail
        self._transaction = transaction_processor
        self._parser = Parser()
        self._output_dir = output_dir   # TODO: abstract this to data.py
        self._transaction_dir = transaction_dir # TODO: abstract this to data.py
        self._action_to_method_map = {
            ActionTypes.nomatch: self._process_nomatch,
            ActionTypes.bodycomposition: self._process_bodycomposition,
            ActionTypes.event: self._process_event,
            ActionTypes.note: self._process_note,
            ActionTypes.todo: self._process_todo,
            ActionTypes.transaction: self._process_transaction
        }
