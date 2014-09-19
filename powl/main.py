#!/usr/bin/env python
"""Main script for running powl."""
import injector
import sys
from powl import action
from powl import retriever

class App:
    """
    Contains the main logic for this app.
    """

    def __init__(self, injector):
        """
        Parameters
        ----------
        injector : injector.Injector
            Container used to resolve objects to run the app.
        """
        self._retriever = injector.get(retriever.Retriever)
        self._action_manager = injector.get(action.ActionManager)

    def run(self):
        """
        Retrieve a list of input actions and perform them.
        """
        items = self._retriever.get_action_items()
        for item, date in items:
            self._action_manager.do_action(item, date)

def main(*args):
    injector = injector.Injector()
    app = App(injector)
    app.run()

if __name__ == '__main__':
    main(*sys.argv[1:])

