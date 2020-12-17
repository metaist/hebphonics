#!/usr/bin/env python
# coding: utf-8
"""Test Hebrew syllabification."""

# pkg
from hebphonics.grammar import Parser


def test_empty():
    """syllabify an empty string"""
    p = Parser()
    assert [] == p.syllabify(p.parse(""))


def test_break_before_vowel():
    """syllable break before a vowel (syllable-before-vowel)"""
    word = r"בָּרָא"  # ba-ra
    parts = [
        ["bet", "dagesh-qal", "qamats-gadol"],
        ["resh", "qamats-gadol", "eim-qria-alef"],
    ]
    p = Parser()
    assert parts == p.syllabify(p.parse(word))


def test_break_before_after_sheva_na():
    """syllable break before and after `sheva-na` (syl-around-sheva-na)"""
    word = r"יֵשְׁבוּ"  # yei-she-vu
    parts = [["yod", "tsere"], ["shin", "sheva-na"], ["vet", "shuruq"]]
    p = Parser()
    assert parts == p.syllabify(p.parse(word))

    word = r"בְּלִי"  # be-li (traditional); bli (modern; TODO)
    parts = [
        ["bet", "dagesh-qal", "sheva-na"],
        ["lamed", "hiriq-male-yod", "eim-qria-yod"],
    ]
    p = Parser()
    assert parts == p.syllabify(p.parse(word))


def test_no_break_sheva_nah():
    """no syllable break after `sheva-nah`"""
    word = r"יִשְׁרְצוּ"
    parts = [
        ["yod", "hiriq", "shin", "sheva-nah"],
        ["resh", "sheva-na"],
        ["tsadi", "shuruq"],
    ]
    p = Parser()
    assert parts == p.syllabify(p.parse(word))


def test_strict_no_break_after_hataf():
    """(strict) no syllable break after hataf-vowel (syl-none-after-hataf)"""
    word = "אֲשֶׁר"
    parts = [["alef", "hataf-patah"], ["shin", "segol", "resh"]]
    p = Parser()
    assert parts == p.syllabify(p.parse(word))

    parts = [["alef", "hataf-patah", "shin", "segol", "resh"]]
    p = Parser()
    assert parts == p.syllabify(p.parse(word), strict=True)


def test_simple_syllables():
    """simple syllables"""
    word = r"מַת"
    parts = [["mem", "patah", "sav"]]
    p = Parser()
    assert parts == p.syllabify(p.parse(word)), "simple closed syllable"

    word = r"מִי"
    parts = [["mem", "hiriq-male-yod", "eim-qria-yod"]]
    p = Parser()
    assert parts == p.syllabify(p.parse(word)), "simple open syllable"
