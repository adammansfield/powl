#!/usr/bin/env python
"""Main script for running powl."""
import sys
from powl.app import App

def main(*args):
    """Create an instance of powl and process a mailbox."""
    app = App()
    app.start()

if __name__ == '__main__':
    main(*sys.argv[1:])
