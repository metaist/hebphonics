#!/usr/bin/python
# coding: utf-8

import unittest

from hebphonics import codes


class TestCodes(unittest.TestCase):
    def test_names(self):
        """Expected to parse names correctly."""
        test = codes.to_names(u'בְּ/רֵאשִׁית')
        expected = [
            'LETTER_BET', 'POINT_DAGESH_OR_MAPIQ', 'POINT_SHEVA', 'SOLIDUS',
            'LETTER_RESH', 'POINT_TSERE', 'LETTER_ALEF', 'LETTER_SHIN',
            'POINT_SHIN_DOT', 'POINT_HIRIQ', 'LETTER_YOD', 'LETTER_TAV'
        ]
        self.assertEqual(test, expected)
