#!/usr/bin/env python
"""Main script for running powl."""
import sys
from powl.controller import Controller

def main(*args):
    """Create an instance of powl and process a mailbox."""
    controller = Controller()
    controller.start()

if __name__ == '__main__':
    main(*sys.argv[1:])
