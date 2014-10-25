#!/usr/bin/env python
import os
import time
import unittest
from powl import actionretriever
from powl import exception
try:
    from test.config import imapconfig
except ImportError:
    cfg_path = os.path.join("test", "config", "imapconfig.py")
    with open(cfg_path, 'a') as cfg_file:
        cfg_file.write("server = \"<enter server here>\"" + os.linesep)
        cfg_file.write("user = \"<enter user here>\"" + os.linesep)
        cfg_file.write("password = \"<enter password here>\"" + os.linesep)
        cfg_file.write("mailbox = \"<enter mailbox here>\"" + os.linesep)
    from test.config import imapconfig


class ImapMailTest(unittest.TestCase):

    def setUp(self):
        self._imap = actionretriever.ImapMail(imapconfig.mailbox)

    def test__connect__success(self):
        """
        Test that IMAP object successfully connects to server.
        """
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()

