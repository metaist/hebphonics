#!/usr/bin/python
# coding: utf-8

import unittest

from hebphonics import db


class TestDB(unittest.TestCase):
    def test_connect(self):
        """Expected to return sessionmaker."""
        test = db.connect(':memory:')
        self.assertTrue(test is not None)
