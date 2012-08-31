#!/usr/bin/python
# coding: utf-8

import unittest

from sqlalchemy.orm.session import Session

from hebphonics import db


class TestDB(unittest.TestCase):
    def test_connect(self):
        """Expected to return a session."""
        test = db.connect(database=db.DEFAULT_DB)
        self.assertTrue(test is not None)
        self.assertTrue(isinstance(test, Session))
