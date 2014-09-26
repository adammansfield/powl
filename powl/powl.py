#!/usr/bin/env python
"""Main script for running powl."""
import injector
import sys
from powl import action
from powl import log
from powl import parser
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
        self._action_manager = injector.get(action.ActionManager)
        self._log = injector.get(log.Log)
        self._parser = injector.get(parser.ActionItemParser)
        self._retriever = injector.get(retriever.ActionItemRetriever)

    def run(self):
        """
        Retrieve a list of input actions and perform them.
        """
        try:
            items = self._retriever.get_action_items()
        except Exception as err:
            message = exception.get_message(err)
            traceback = traceback.format_exc()
            log_.error(message)
            log_.debug(traceback)
        else:
            for item, date in items:
                try:
                    log_message = "action ({0}) on {1}".format(
                        item, time.strftime("%Y-%m-%d", date))
                    self._log.info(log_message)
                    action_key, action_data = self._parser.parse(item)
                    self._action_manager.do_action(action_key, action_data,
                                                   date)
                except Exception as err:
                    message = exception.get_message(err)
                    traceback = traceback.format_exc()
                    log_.error(message)
                    log_.debug(traceback)

def main(*args):
    injector = injector.Injector()
    app = App(injector)
    app.run()

if __name__ == '__main__':
    main(*sys.argv[1:])

