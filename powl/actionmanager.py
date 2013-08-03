"""Perform actions with given data."""
from powl import actiontype

class ActionManager:
    """
    Provides methods for doing actions.
    """

    def __init__(
        self,
        log,                     # powl.logwriter.LogWriter
        accounting_action,       # powl.actions.accounting.Accounting
        body_composition_action, # powl.actions.body_composition.BodyComposition
        note_action):            # powl.actions.note.Note
        """
        Initialize action map.

        Args:
            log: Used to log.
            accounting_action: Performs an accounting action.
            body_composition_action: Performs a body composition action.
            note_action: Performs a note action.
        """
        self._log = log
        self._accounting_action = accounting_action
        self._body_composition_action = body_composition_action
        self._note_action = note_action

        self._action_type_to_action_map = {
            actiontype.ACCOUNTING: self._accounting_action,
            actiontype.BODYCOMPOSITION: self._bodycomposition_action,
            actiontype.NOTE: self._note_action
        }

    def do_action(self, action_type, action_data):
        """
        Do the specified action.

        Args:
            action_type: The type of action to do.
            data: Action specific class containing all data required for the
                specified action type.
        """
        try:
            action = self._action_type_to_action_map[action_type]
        except KeyError as e:
            self._log.error(
                "Action type '%s' is not in the action map",
                action_type)

       try:
            action.do(action_data)
       except ValueError as e:
            self._log.error(
                "ValueError was raised by action '%s' with the message '%s'",
                action_type,
                e)
       except IOError as e:
            self._log.error(
                "IOError was raised by action '%s' with the message '%s'",
                action_type,
                e)
