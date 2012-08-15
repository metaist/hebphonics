#!/usr/bin/python
# coding: utf-8

import unittest

from hebphonics import hebrew


class TestHebrew(unittest.TestCase):

    def test_groups(self):
        """Expected to group characters."""
        test = hebrew.groups([
            'LETTER_BET', 'POINT_DAGESH_OR_MAPIQ', 'POINT_SHEVA', 'SOLIDUS',
            'LETTER_RESH', 'POINT_TSERE', 'LETTER_ALEF', 'LETTER_SHIN',
            'POINT_SHIN_DOT', 'POINT_HIRIQ', 'LETTER_YOD', 'LETTER_TAV'
        ])
        expected = [
            ['LETTER_BET', 'POINT_DAGESH_OR_MAPIQ', 'POINT_SHEVA'],
            ['SOLIDUS'], ['LETTER_RESH', 'POINT_TSERE'], ['LETTER_ALEF'],
            ['LETTER_SHIN', 'POINT_SHIN_DOT', 'POINT_HIRIQ'], ['LETTER_YOD'],
            ['LETTER_TAV']
        ]
        self.assertEqual(test, expected)
