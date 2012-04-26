#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.getcwd()))
import powl

class ParseTest(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.dirname(os.getcwd()))
        self.powl = powl.Powl()

    def test_markup_strip(self):
        teststring = "<P>This is a test string.=0AA &amp; B.</P>"
        expected = "This is a test string. A & B."
        actual = self.powl.strip_message_markup(teststring)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
