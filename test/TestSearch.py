#!/usr/bin/python
# coding: utf-8

import os
import re
import unittest

from sqlalchemy.orm.session import Session

from hebphonics import db, search


class TestSearch(unittest.TestCase):
    session = None

    def setUp(self):
        """Setup connection."""
        path = os.path.join('db', 'hebphonics.db')
        self.session = db.connect(database=path)

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