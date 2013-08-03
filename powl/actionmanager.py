"""Perform actions with given data."""
from powl.actions import action_types

class ActionPerformer:
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
            action_types.ActionTypes.ACCOUNTING: self._accounting_action,
            action_types.ActionTypes.BODYCOMPOSITION: self._bodycomposition_action,
            action_types.ActionTypes.INDETERMINATE: self._note_action,
            action_types.ActionTypes.NOTE: self._note_action
        }

    def do_action(self, action_type, action_data):
        """
        Do the specified action.

        Args:
            action_type: The type of action to do.
            data: Action specific class containing all data required for the
                specified action type.
        """
        if action_type == action_types.ActionTypes.INDETERMINATE:
            self._log.error("Action type is indeterminate", action_type)
        else:
            try:
                action = self._action_type_to_action_map[action_type]
                action.do(action_data)
            except KeyError as e:
                self._log.error(
                    "Action type '%s' is not in the action type to action map",
                    action_type
                )
