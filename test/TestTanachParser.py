#!/usr/bin/python
# coding: utf-8

import os
import unittest

from hebphonics.parsers import tanach


class TestTanachParser(unittest.TestCase):

    def test_parse_texts(self):
        """Expected to parse basic texts."""
        test = tanach.parse(os.path.join('test', 'texts'), 'Index.xml')
        self.assertIs(type(test), dict)
        self.assertTrue(len(test) > 0)
