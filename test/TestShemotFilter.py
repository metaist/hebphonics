#!/usr/bin/python
# coding: utf-8

import unittest

from hebphonics.filters import ShemotFilter


class TestShemotFilter(unittest.TestCase):
    def test_filter(self):
        """Expected to filter names of God."""
        test = u'אֱלֹהִים'
        self.assertTrue(ShemotFilter.matches(test))

        test = u'בֵאלֹהִים'
        self.assertTrue(ShemotFilter.matches(test))

        test = u'אֱלוֹהֵי'
        self.assertTrue(ShemotFilter.matches(test))

        test = u'אֱלוֹהַי'
        self.assertTrue(ShemotFilter.matches(test))

        test = u'אֵל'
        self.assertTrue(ShemotFilter.matches(test))

        test = u'אֵלַי'
        self.assertFalse(ShemotFilter.matches(test), 'should not match')
