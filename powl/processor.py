#!/usr/bin/env python
"""Parse actions and processing for simpler actions."""

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
