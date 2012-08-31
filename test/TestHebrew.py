#!/usr/bin/python
# coding: utf-8

import unittest

from hebphonics import hebrew


class TestHebrew(unittest.TestCase):
    def test_syllabify(self):
        """Expected to syllabify strings."""
        test = hebrew.syllabify(u'מַת')
        expected = [['mem', 'patah', 'sav']]
        self.assertEqual(test, expected, 'simple closed syllable')

        test = hebrew.syllabify(u'מִי')
        expected = [['mem', 'hiriq-male', 'yod']]
        self.assertEqual(test, expected, 'simple open syllable')

        test = hebrew.syllabify(u'לָרֶדֶת')
        expected = [['lamed', 'qamats'],
                    ['resh', 'segol'],
                    ['dalet', 'segol', 'sav']]
        self.assertEqual(test, expected, 'simple word')

        test = hebrew.syllabify(u'בְּ/רֵאשִׁית')
        expected = [['bet', 'dagesh-qal', 'sheva-na', 'resh', 'tsere', 'alef'],
                    ['shin', 'hiriq-male', 'yod', 'sav']]
        self.assertEqual(test, expected, 'should parse basic word')

        test = hebrew.syllabify(u'אֶֽעֱשֶׂהּ־')
        expected = [['alef', 'segol'],
                    ['ayin', 'hataf-segol'],
                    ['sin', 'segol', 'mapiq-he', 'mapiq']]
        self.assertEqual(test, expected, 'hatafs in own syllables')

        test = hebrew.syllabify(u'אֶֽעֱשֶׂהּ־', hataf_own=False)
        expected = [['alef', 'segol'],
                    ['ayin', 'hataf-segol', 'sin', 'segol',
                    'mapiq-he', 'mapiq']]
        self.assertEqual(test, expected, 'hatafs merged with next syllable')

        test = hebrew.syllabify(u'וַ/יִּתְפְּרוּ')
        expected = [['vav', 'patah'],
                    ['yod', 'dagesh-hazaq', 'hiriq'],
                    ['sav', 'sheva-nah'],
                    ['pe', 'dagesh-qal', 'sheva-na', 'resh', 'shuruq']]
        self.assertEqual(test, expected, 'sheva-nah breaks syllable')

    def test_parse_basic(self):
        """Expected to parse strings."""
        test = hebrew.parse(u'בְּ/רֵאשִׁית')
        expected = ['bet', 'dagesh-qal', 'sheva-na', 'resh', 'tsere', 'alef',
                    'shin', 'hiriq-male', 'yod', 'sav']
        self.assertEqual(test, expected)

    def test_mapiq(self):
        """Expected to parse mapiq letters."""
        test = hebrew.parse(u'אֶֽעֱשֶׂהּ־')
        expected = ['alef', 'segol', 'ayin', 'hataf-segol', 'sin', 'segol',
                    'mapiq-he', 'mapiq']
        self.assertEqual(test, expected, 'when mapiq-he')

        test = hebrew.parse(u'וַ/יָּבִ֥יאּוּ')
        expected = ['vav', 'patah', 'yod', 'dagesh-hazaq', 'patah', 'vet',
                    'hiriq-male', 'yod', 'mapiq-alef', 'mapiq', 'shuruq']

    def test_parse_begedkefet(self):
        """Expected to parse BeGeDKeFeT letters."""
        test = hebrew.parse(u'הַ/שָּׁמַיִם')
        expected = ['he', 'patah', 'shin', 'dagesh-hazaq', 'qamats', 'mem',
                    'patah', 'yod', 'hiriq', 'mem-sofit']
        self.assertEqual(test, expected)

        test = hebrew.parse(u'הַ/גְּדֹלִים')
        expected = ['he', 'patah', 'gimel', 'dagesh-hazaq', 'sheva-na',
                    'dalet', 'holam-haser', 'lamed', 'hiriq-male', 'yod',
                    'mem-sofit']
        self.assertEqual(test, expected)

        test = hebrew.parse(u'בְּ/תוֹךְ')
        expected = ['bet', 'dagesh-qal', 'sheva-na', 'sav', 'holam-male',
                    'khaf-sofit', 'sheva-nah']
        self.assertEqual(test, expected)

        test = hebrew.parse(u'כִּי')
        expected = ['kaf', 'dagesh-qal', 'hiriq-male', 'yod']
        self.assertEqual(test, expected)

        test = hebrew.parse(u'נֶפֶשׁ')
        expected = ['nun', 'segol', 'fe', 'segol', 'shin']
        self.assertEqual(test, expected)

    def test_parse_pe_sofit(self):
        """Expected to parse pe-sofit (rare letter)."""
        test = hebrew.parse(u'תּוֹסְףְּ')
        expected = ['tav', 'dagesh-qal', 'holam-male', 'samekh', 'sheva-na',
                    'pe-sofit', 'dagesh-qal', 'sheva-nah']
        self.assertEqual(test, expected)

    def test_parse_shuruq(self):
        """Expected to parse shuruq."""
        test = hebrew.parse(u'וּ/בַ/לַּיְלָה')
        expected = ['shuruq', 'vet', 'patah', 'lamed', 'dagesh-hazaq', 'patah',
                    'yod', 'sheva', 'lamed', 'qamats', 'he']
        self.assertEqual(test, expected)

    def test_parse_vav_dagesh_vowel(self):
        """Expected to parse vav, dagesh, {vowel}."""
        test = hebrew.parse(u'אִוָּשֵׁעַ')
        expected = ['alef', 'hiriq', 'vav', 'dagesh-hazaq', 'qamats', 'shin',
                    'tsere', 'ayin', 'patah-genuvah']
        self.assertEqual(test, expected)

    def test_parse_vav_dagesh_holam_haser(self):
        """Expected to parse vav, dagesh, holam-haser."""
        test = hebrew.parse(u'קַוֹּה')
        expected = ['qof', 'patah', 'vav', 'dagesh-hazaq', 'holam-haser', 'he']
        self.assertEqual(test, expected)

    def test_parse_holam_haser_for_vav(self):
        """Expected to parse holam-haser for vav (unicode code point)."""
        test = hebrew.parse(u'עֲוֺנִ/י')
        expected = ['ayin', 'hataf-patah', 'vav', 'holam-haser', 'nun',
                    'hiriq-male', 'yod']
        self.assertEqual(test, expected)

    def test_parse_double_sheva(self):
        """Expected to parse double-sheva."""
        test = hebrew.parse(u'וַ/יִּתְפְּרוּ')
        expected = ['vav', 'patah', 'yod', 'dagesh-hazaq', 'hiriq', 'sav',
                    'sheva-nah', 'pe', 'dagesh-qal', 'sheva-na', 'resh',
                    'shuruq']
        self.assertEqual(test, expected)

    def test_parse_qamats_qatan(self):
        """Expected to parse qamats-qatan."""
        test = hebrew.parse(u'אָהֳלֹ/ה')
        expected = ['alef', 'qamats-qatan', 'he', 'hataf-qamats', 'lamed',
                    'holam-haser', 'he']
        self.assertEqual(test, expected, 'when precedes hataf-qamats')

        test = hebrew.parse(u'וּ/בְ/כָל־')
        expected = ['shuruq', 'vet', 'sheva-na', 'khaf', 'qamats-qatan',
                    'lamed']
        self.assertEqual(test, expected, 'when ends-in-maqaf')
