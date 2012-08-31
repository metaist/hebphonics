#!/usr/bin/python
# coding: utf-8

import os
import unittest

from hebphonics.parsers import TanachParser


class TestTanachParser(unittest.TestCase):
    def test_parse_texts(self):
        """Expected to parse basic texts."""
        test = TanachParser.parse(os.path.join('test', 'texts'), 'Index.xml')
        self.assertTrue(type(test) is dict)
        self.assertTrue(len(test) > 0)
