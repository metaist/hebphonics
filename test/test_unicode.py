#!/usr/bin/env python
# coding: utf-8
"""Unicode tests."""

# pkg
from hebphonics import tokens as T


def test_normalize():
    """normalize unicode symbols"""
    want = T.LETTER_ALEF + T.POINT_DAGESH_OR_MAPIQ
    test = T.normalize(T.LETTER_ALEF_WITH_MAPIQ)
    assert test == want

    want = T.LETTER_AYIN
    test = T.normalize(T.LETTER_ALTERNATIVE_AYIN)
    assert test == want

    want = T.LETTER_ALEF
    test = T.normalize(T.LETTER_WIDE_ALEF)
    assert test == want

    want = T.PUNCTUATION_NUN_HAFUKHA
    test = T.normalize(T.PUNCTUATION_NUN_HAFUKHA)
    assert test == want


def test_names():
    """unicode symbol names"""
    test = [T.uniname(char, mode="const") for char in u"בְּ/רֵאשִׁית"]
    want = [
        "LETTER_BET",
        "POINT_DAGESH_OR_MAPIQ",
        "POINT_SHEVA",
        "SOLIDUS",
        "LETTER_RESH",
        "POINT_TSERE",
        "LETTER_ALEF",
        "LETTER_SHIN",
        "POINT_SHIN_DOT",
        "POINT_HIRIQ",
        "LETTER_YOD",
        "LETTER_TAV",
    ]
    assert test == want
