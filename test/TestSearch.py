#!/usr/bin/python
# coding: utf-8

import os
import re
import unittest

from sqlalchemy.orm.session import Session

from hebphonics import db, hebrew, search
from hebphonics.parsers import TanachParser


class TestSearch(unittest.TestCase):

    #def setUp(self):
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
        query = search.search(self.session, search_books='2 TestBook')
        test = query.all()
        self.assertTrue(len(test) > 0)

        query = search.search(self.session,
                              search_books=['1 TestBook', '2 TestBook'])
        test = query.all()
        self.assertTrue(len(test) > 0)

    def test_shemot_search_and_filter(self):
        """Expected to search and filter out shemot."""
        query = search.search(self.session, search_shemot=True)
        for test in query:
            self.assertTrue(hebrew.isshemot(test.hebrew))

        query = search.search(self.session, filter_shemot=True)
        for test in query:
            self.assertFalse(hebrew.isshemot(test.hebrew))

    def test_letter_filters(self):
        """Expected to filter words based on letter criteria."""
        value = 'alef'
        query = search.search(self.session, letters_any=value)
        for test in query:
            self.assertTrue(value in test.syllables)

        value = ['alef', 'bet']
        query = search.search(self.session, letters_any=value)
        for test in query:
            self.assertTrue(value[0] in test.syllables or
                            value[1] in test.syllables)

        value = ['alef', 'bet']
        query = search.search(self.session, letters_all=value)
        for test in query:
            self.assertTrue(value[0] in test.syllables and
                            value[1] in test.syllables)

        value = ['alef', 'bet']
        query = search.search(self.session, letters_none=value)
        for test in query:
            self.assertTrue(value[0] not in test.syllables and
                            value[1] not in test.syllables)

        value = ['resh', 'alef', 'shin']
        query = search.search(self.session, letters_seq=value)
        for test in query:
            self.assertTrue(value[0] in test.syllables and
                            value[1] in test.syllables and
                            value[2] in test.syllables)

    def test_gematria_filter(self):
        """Expected to filter words based on gematria."""
        value = 10
        query = search.search(self.session, filter_gematria=value)
        for test in query:
            self.assertTrue(test.gematria, hebrew.gematria(test.hebrew))

        value = (10, 20)
        query = search.search(self.session, filter_gematria=value)
        for test in query:
            gematria = hebrew.gematria(test.hebrew)
            print gematria
            self.assertTrue(10 < gematria < 20)

        value = [10, 20]
        query = search.search(self.session, filter_gematria=value)
        for test in query:
            gematria = hebrew.gematria(test.hebrew)
            self.assertTrue(10 <= gematria <= 20)

        value = {'__gt__': 10, '__le__': 20}
        query = search.search(self.session, filter_gematria=value)
        for test in query:
            gematria = hebrew.gematria(test.hebrew)
            self.assertTrue(10 < gematria <= 20)

    def test_syllen_filter(self):
        """Expected to filter words based on syllable length."""
        value = 1
        query = search.search(self.session, filter_syllen=value)
        for test in query:
            self.assertEqual(test.syllen, 1)

        value = [1]
        query = search.search(self.session, filter_syllen=value)
        for test in query:
            self.assertEqual(test.syllen, 1)

        value = 2
        query = search.search(self.session, filter_syllen_hatafs=value)
        for test in query:
            self.assertEqual(test.syllen_hatafs, 2)

        value = [2]
        query = search.search(self.session, filter_syllen_hatafs=value)
        for test in query:
            self.assertEqual(test.syllen_hatafs, 2)

        value = [2, 3]
        query = search.search(self.session, filter_syllen_hatafs=value)
        for test in query:
            self.assertTrue(test.syllen_hatafs in value)
