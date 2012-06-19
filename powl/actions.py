#!/usr/bin/env python
"""Perform actions with given data."""
from powl.transaction import Transaction

class Actions:
    """Contains definitions for possible actions."""
    nomatch = 'nomatch'
    bodycomposition = 'bodycomposition'
    event = 'event'
    note = 'note'
    todo = 'todo'
    transaction = 'transaction'
    actionable_list = [
        action_bodycomposition,
        action_event,
        action_note,
        action_todo,
        action_transaction
    ]


    def do_action(self, action, data, date):
        """Determine and do the specified action."""
        self._action_to_method_map[action](data, date)

    def _process_bodycomposition(self, data, date):
        pass

    def _process_event(self, data, date):
        pass

    def _process_note(self, data, date):
        pass

    def _process_nomatch(self, data, date):
        pass

    def _process_todo(self, data, date):
        pass

    def _process_transaction(self, data, date):
        """Separate transaction data to pass onto processing."""
        debit, credit, amount, memo = self.message.transaction(params)
        filename, data = self.transaction.process(date, debit, credit, amount, memo)
        output.append(filename, data)

    def __init__(self, config):
        self._config = config
        self._transaction = Transaction(self._config.qif_filenames,
                                        self._config.qif_types,
                                        self._config.qif_assets,
                                        self._config.qif_liabilities,
                                        self._config.qif_revenues,
                                        self._config.qif_expenses)
        self._action_to_method_map = {
            self.nomatch: self._process_nomatch,
            self.bodycomposition: self._process_bodycomposition,
            self.event: self._process_event,
            self.note: self._process_note,
            self.todo: self._process_todo,
            self.transaction: self._process_transaction
        }
