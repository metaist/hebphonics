#!/usr/bin/python
"""`sheva-`"""

# pkg
from hebphonics.grammar import Parser


def test_sheva_na_start():
    """`sheva` at word start is `sheva-na` (sheva-na-word-start)"""
    word = r"וְאֵת"  # ve-et
    parts = ["vav", "sheva-na", "alef", "tsere", "sav"]
    assert parts == Parser().parse(word).flat()

    word = r"קְדוֹשׁ"  # ke-dosh
    parts = ["qof", "sheva-na", "dalet", "holam-male-vav", "shin"]
    assert parts == Parser().parse(word).flat()

    word = r"בְּלִי"  # be-li
    parts = ["bet", "dagesh-qal", "sheva-na", "lamed", "hiriq-male-yod", "yod"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_end():
    """`sheva` at the end of a word is `sheva-nah` (sheva-nah-word-end)"""
    word = r"הַחֹשֶׁךְ"  # ha-chosh
    parts = [
        "he",
        "patah",
        "het",
        "holam-haser",
        "shin",
        "segol",
        "khaf-sofit",
        "sheva-nah",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_under_dagesh_hazaq():
    """`sheva` under `dagesh-hazaq` is `sheva-na` (sheva-na-dagesh-hazaq)"""
    word = r"הַמְּאֹרֹת"  # ha-me-orth
    parts = [
        "he",
        "patah",
        "mem",
        "dagesh-hazaq",
        "sheva-na",
        "alef",
        "holam-haser",
        "resh",
        "holam-haser",
        "sav",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_after_long_vowel():
    """H204: `sheva` after long vowel is `sheva-na` (sheva-na-after-long-vowel)"""
    word = r"הָיְתָה"  # hay-tah
    parts = ["he", "qamats-gadol", "yod", "sheva-na", "sav", "qamats-male-he", "he"]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_after_holam_alef():
    """H204: `sheva` after long vowel is `sheva-na` (sheva-na-after-long-vowel)
    (including holam+alef)
    """
    word = r"תֹּאמְרוּ"  # tom-ru
    parts = [
        "tav",
        "dagesh-qal",
        "holam-male-alef",
        "alef",
        "mem",
        "sheva-na",
        "resh",
        "shuruq",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_after_short_vowel():
    """H205: `sheva` after short vowel is `sheva-nah` (sheva-nah-after-short-vowel)"""
    word = r"פַּרְעֹה"  # par-oh
    parts = [
        "pe",
        "dagesh-qal",
        "patah",
        "resh",
        "sheva-nah",
        "ayin",
        "holam-male-he",
        "he",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"נֶאֱסְפוּ"  # ne-eh-sfu
    parts = [
        "nun",
        "segol",
        "alef",
        "hataf-segol",
        "samekh",
        "sheva-nah",
        "fe",
        "shuruq",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_alef_end():
    """H206: `sheva` before last bare `alef` is `sheva-nah` (sheva-nah-alef-end)"""
    word = "חֵטְא"  # heit
    parts = ["het", "tsere", "tet", "sheva-nah", "alef"]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_before_same_sounding_letter():
    """H207: `sheva` before same letter is `sheva-na` (sheva-na-double-letter)"""
    word = r"הַלְלוּ"  # ha-le-lu
    parts = ["he", "patah", "lamed", "sheva-na", "lamed", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_double_sheva_middle():
    """H208: two `sheva` midword are `sheva-nah`, `sheva-na` (sheva-double-midword)"""
    word = r"עֶזְרְךָ"  # ez-rcha
    parts = [
        "ayin",
        "segol",
        "zayin",
        "sheva-nah",
        "resh",
        "sheva-na",
        "khaf-sofit",
        "qamats",
    ]
    assert parts == Parser().parse(word).flat()


def test_double_sheva_end():
    """H209: two `sheva` at word end are `sheva-na`, `sheva-na` (sheva-double-end)"""
    word = r"וְיֵשְׁתְּ"  # va-yeisht
    parts = [
        "vav",
        "sheva-na",
        "yod",
        "tsere",
        "shin",
        "sheva-na",
        "tav",
        "dagesh-qal",
        "sheva-na",
    ]
    assert parts == Parser().parse(word).flat()


def test_not_real_sheva():
    """an unknown kind of sheva"""
    word = r"זרְע"
    parts = ["zayin", "resh", "sheva", "ayin"]
    assert parts == Parser().parse(word).flat()
