"""Defines action types and an action map for shorthand keys."""

# Action types.
BODY_COMPOSITION = "bodycomposition"
NOTE = "note"
TRANSACTION = "transaction"

# Maps keys to actions. Multiple keys can map to one action.
ACTION_MAP = {
    "b": BODY_COMPOSITION,
    "body": BODY_COMPOSITION,
    "bodycomposition": BODY_COMPOSITION,

    "n": NOTE,
    "note": NOTE,

    "a": TRANSACTION,
    "transaction": TRANSACTION
}

