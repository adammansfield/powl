#!/usr/bin/env python
"""Main script for running powl."""
import sys
from powl.powl import Powl

def main(*args):
    """Create an instance of powl and process a mailbox."""
    powl = Powl()
    powl.process()

if __name__ == '__main__':
    main(*sys.argv[1:])
