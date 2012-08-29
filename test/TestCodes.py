#!/usr/bin/python
# coding: utf-8

import unittest

from hebphonics import codes


class TestCodes(unittest.TestCase):
    def test_normalize(self):
        """Expected to normalize unicode correctly."""
        test = codes.normalize(codes.LETTER_ALEF_WITH_MAPIQ)
        expected = codes.LETTER_ALEF + codes.POINT_DAGESH_OR_MAPIQ
        self.assertEqual(test, expected)

        test = codes.normalize(codes.LETTER_ALTERNATIVE_AYIN)
        expected = codes.LETTER_AYIN
        self.assertEqual(test, expected)

        test = codes.normalize(codes.LETTER_WIDE_ALEF)
        expected = codes.LETTER_ALEF
        self.assertEqual(test, expected)

        test = codes.normalize(codes.PUNCTUATION_NUN_HAFUKHA)
        expected = codes.PUNCTUATION_NUN_HAFUKHA
        self.assertEqual(test, expected)

    def test_names(self):
        """Expected to parse names correctly."""
        test = [codes.name(char, mode='const') for char in u'בְּ/רֵאשִׁית']
        expected = [
            'LETTER_BET', 'POINT_DAGESH_OR_MAPIQ', 'POINT_SHEVA', 'SOLIDUS',
            'LETTER_RESH', 'POINT_TSERE', 'LETTER_ALEF', 'LETTER_SHIN',
            'POINT_SHIN_DOT', 'POINT_HIRIQ', 'LETTER_YOD', 'LETTER_TAV'
        ]
        self.assertEqual(test, expected)
