#!/usr/bin/python
# coding: utf-8

import os
import re
import unittest

from sqlalchemy.orm.session import Session

from hebphonics import db, hebrew, search
from hebphonics.parsers import TanachParser


class TestSearch(unittest.TestCase):

    def __init__(self, *args):
        """Setup connection."""
        unittest.TestCase.__init__(self, *args)
        self.session = db.connect(database=db.DEFAULT_DB, debug=True)
        root = os.path.join('test', 'texts')
        TanachParser.parse(self.session, root, 'Index.xml')

    def test_no_filter(self):
        """Expected to do basic search."""
        limit = 10
        query = search.search(self.session, limit=limit)
        test = [item for item in query]
        self.assertEqual(len(test), limit)

    def test_search_books(self):
        """Expected to search within certain books."""
        query = search.search(self.session, books='2 TestBook')
        test = query.all()
        self.assertTrue(len(test) > 0)

        query = search.search(self.session, books=['1 TestBook', '2 TestBook'])
        test = query.all()
        self.assertTrue(len(test) > 0)

    def test_shemot_filter(self):
        """Expected to filter out shemot."""
        query = search.search(self.session, shemot=False)
        for test in query:
            self.assertFalse(hebrew.isshemot(test.hebrew))

        query = search.search(self.session, shemot=True)
        expected = [hebrew.isshemot(test.hebrew) for test in query]
        self.assertTrue(sum(expected) > 0, 'expected at least one name of G-d')

    def test_letter_filters(self):
        """Expected to filter words based on letter criteria."""
        value = 'alef'
        query = search.search(self.session, find_any=value)
        for test in query:
            self.assertTrue(value in test.syllables)

        value = ['alef', 'bet']
        query = search.search(self.session, find_any=value)
        for test in query:
            self.assertTrue(value[0] in test.syllables or
                            value[1] in test.syllables)

        value = ['alef', 'bet']
        query = search.search(self.session, find_all=value)
        for test in query:
            self.assertTrue(value[0] in test.syllables and
                            value[1] in test.syllables)

        value = ['alef', 'bet']
        query = search.search(self.session, find_none=value)
        for test in query:
            self.assertTrue(value[0] not in test.syllables and
                            value[1] not in test.syllables)

        value = ['resh', 'alef', 'shin']
        query = search.search(self.session, find_seq=value)
        for test in query:
            self.assertTrue(value[0] in test.syllables and
                            value[1] in test.syllables and
                            value[2] in test.syllables)

    def test_gematria_filter(self):
        """Expected to filter words based on gematria."""
        value = 10
        query = search.search(self.session, gematria=value)
        for test in query:
            self.assertTrue(test.gematria, hebrew.gematria(test.hebrew))

        value = [10, 20]
        query = search.search(self.session, gematria=value)
        for test in query:
            gematria = hebrew.gematria(test.hebrew)
            self.assertTrue(10 == gematria or
                            20 == gematria)

    def test_syllen_filter(self):
        """Expected to filter words based on syllable length."""
        value = 1
        query = search.search(self.session, syllen=value)
        for test in query:
            self.assertEqual(test.syllen, 1)

        value = [1]
        query = search.search(self.session, syllen=value)
        for test in query:
            self.assertEqual(test.syllen, 1)

        value = 2
        query = search.search(self.session, syllen_hatafs=value)
        for test in query:
            self.assertEqual(test.syllen_hatafs, 2)

        value = [2]
        query = search.search(self.session, syllen_hatafs=value)
        for test in query:
            self.assertEqual(test.syllen_hatafs, 2)

        value = [2, 3]
        query = search.search(self.session, syllen_hatafs=value)
        for test in query:
            self.assertTrue(test.syllen_hatafs in value)
