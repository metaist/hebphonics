#!/usr/bin/env python
# coding: utf-8
"""Test Hebrew syllabification."""

# pkg
from hebphonics.grammar import Parser


def test_empty():
    """syllabify an empty string"""
    p = Parser("")
    p.parse()
    assert p.syllabify() == []


def test_break_before_vowel():
    """H001: syllable break before a vowel (syl-before-vowel)"""
    word = r"בָּרָא"
    parts = [["bet", "dagesh-qal", "qamats"], ["resh", "qamats-male", "alef"]]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify()


def test_break_before_after_sheva_na():
    """H002: syllable break before and after `sheva-na` (syl-around-sheva-na)"""
    word = r"שָׁרְצוּ"
    parts = [["shin", "qamats"], ["resh", "sheva-na"], ["tsadi", "shuruq"]]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify()

    word = r"בְּלִי"
    parts = [["bet", "dagesh-qal", "sheva-na"], ["lamed", "hiriq-male", "yod"]]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify()


def test_no_break_sheva_nah():
    """!H002: no syllable break after `sheva-nah`"""
    word = r"יִשְׁרְצוּ"
    parts = [
        ["yod", "hiriq", "shin", "sheva-nah"],
        ["resh", "sheva-na"],
        ["tsadi", "shuruq"],
    ]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify()


def test_strict_no_break_after_hataf():
    """H003: (strict) no syllable break after hataf-vowel (syl-none-after-hataf)"""
    word = "אֲשֶׁר"
    parts = [["alef", "hataf-patah"], ["shin", "segol", "resh"]]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify()

    parts = [["alef", "hataf-patah", "shin", "segol", "resh"]]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify(strict=True)


def test_simple_syllables():
    """simple syllables"""
    word = r"מַת"
    parts = [["mem", "patah", "sav"]]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify(), "simple closed syllable"

    word = r"מִי"
    parts = [["mem", "hiriq-male", "yod"]]
    p = Parser(word)
    p.parse()
    assert parts == p.syllabify(), "simple open syllable"
