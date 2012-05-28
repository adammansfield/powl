#!/usr/bin/env python
"""Main script for running powl."""
import sys
from powl.powl import Powl


def main(*args):
    powl = Powl()
    powl.process_mailbox()


if __name__ == '__main__':
    main(*sys.argv[1:])
