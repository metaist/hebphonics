#!/usr/bin/python
# coding: utf-8

import os
import re
import unittest

from sqlalchemy.orm.session import Session

from hebphonics import db, hebrew, search
from hebphonics.parsers import TanachParser


class TestSearch(unittest.TestCase):
    def setUp(self):
        """Setup connection."""
        self.session = db.connect(database=db.DEFAULT_DB, debug=True)
        root = os.path.join('test', 'texts')
        TanachParser.parse(self.session, root, 'Index.xml')

    def test_no_filter(self):
        """Expected to do basic search."""
        limit = 10
        query = search.search(self.session, limit=limit)
        test = [item for item in query]
        self.assertEqual(len(test), limit)

    def test_shemot_regex(self):
        """Expected to correctly identify names of G-d."""
        regex = re.compile(search.SHEMOT_REGEX, re.I + re.U)

        test = u'אֱלֹהִים'
        self.assertTrue(regex.search(test) is not None)

        test = u'בֵאלֹהִים'
        self.assertTrue(regex.search(test) is not None)

        test = u'אֱלוֹהֵי'
        self.assertTrue(regex.search(test) is not None)

        test = u'אֱלוֹהַי'
        self.assertTrue(regex.search(test) is not None)

        test = u'אֵל'
        self.assertTrue(regex.search(test) is not None)

        test = u'אֵלַי'
        self.assertTrue(regex.search(test) is None, 'should not match')

    def test_shemot_search_and_filter(self):
        """Expected to filter out shemot."""
        regex = re.compile(search.SHEMOT_REGEX, re.I + re.U)
        query = search.search(self.session, search_shemot=True)
        for test in query:
            self.assertTrue(regex.search(test.hebrew) is not None)

        query = search.search(self.session, filter_shemot=True)
        for test in query:
            self.assertTrue(regex.search(test.hebrew) is None)

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
