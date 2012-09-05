#!/usr/bin/python
# coding: utf-8

import os
import unittest

from hebphonics import db
from hebphonics.parsers import TanachParser


class TestTanachParser(unittest.TestCase):
    def setUp(self):
        """Establish a database connection."""
        self.session = db.connect(database=db.DEFAULT_DB, debug=True)

    def test_parse_texts(self):
        """Expected to parse basic texts."""
        root = os.path.join('test', 'texts')
        TanachParser.parse(self.session, root, 'Index.xml')

        books = self.session.query(db.Book).all()
        self.assertEqual(len(books), 2, 'expected to have 2 books')
        self.assertEqual(books[0].name, '1 TestBook', 'expected to get name')
