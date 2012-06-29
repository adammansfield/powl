#!/usr/bin/env python
"""Defines action types."""

class ActionTypes:
    
    # Type when an action does not match
    nomatch = 'nomatch'


    # To process body data such as weight, bodyfat
    bodycomposition = 'bodycomposition'

    # To process events to add to calendar
    event = 'event'

    # To process a note
    note = 'note'

    # To process a task to add to task manager
    todo = 'todo'

    # To process a transaction into accounting database
    transaction = 'transaction'


    # List of valid actions
    actionable = [
        bodycomposition,
        event,
        note,
        todo,
        transaction
    ]
