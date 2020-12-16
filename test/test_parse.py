#!/usr/bin/env python
# coding: utf-8
"""Hebrew grammar parsing."""

# pkg
from hebphonics.grammar import Token, Parser
from hebphonics import tokens as T

DEFAULT_DISABLE = ["qamats-qatan-closed-unaccented"]


def test_lex_accents():
    """lex a string with several things"""
    word = r"וְיִקָּרֵ֤א"
    parts = [
        Token(letter=T.LETTER_VAV, vowel=T.POINT_SHEVA),
        Token(letter=T.LETTER_YOD, vowel=T.POINT_HIRIQ),
        Token(
            letter=T.LETTER_QOF, dagesh=T.POINT_DAGESH_OR_MAPIQ, vowel=T.POINT_QAMATS
        ),
        Token(letter=T.LETTER_RESH, vowel=T.POINT_TSERE, accents=[T.ACCENT_MAHAPAKH]),
        Token(letter=T.LETTER_ALEF),
    ]
    assert parts == Parser.lex(word)


def test_empty():
    """Parse an empty string."""
    assert Parser().parse("") == []


def test_no_rules():
    """a word that doesn't require any special rules"""
    word = r"עַל"  # al
    parts = ["ayin", "patah", "lamed"]
    assert parts == Parser().parse(word).flat()


def test_disable_rules():
    """disabled rule does not run"""
    word = r"רֻאּֽוּ"  # roo'oo
    parts = ["resh", "qubuts", "alef", "dagesh-hazaq", "shuruq"]
    assert parts == Parser(disabled=["dagesh-is-mapiq-alef"]).parse(word).flat()


def test_enabled_rules():
    """only enabled rules run"""
    word = r"נֹחַ"  # no-ah
    parts = ["nun", "holam", "het", "patah-genuvah"]
    enabled, disabled = ["vowel-patah-genuvah"], ["vowel-holam-haser-default"]
    assert parts == Parser(enabled=enabled, disabled=disabled).parse(word).flat()


def test_patah_genuvah():
    """`patah` on last `het|ayin|mapiq-he` is `patah-genuvah` (patah-genuvah)"""
    word = r"נֹחַ"  # no-ah
    parts = ["nun", "holam-haser", "het", "patah-genuvah"]
    assert parts == Parser().parse(word).flat()

    word = r"הָרֵעַ"  # ha-rei-a
    parts = ["he", "qamats-gadol", "resh", "tsere", "ayin", "patah-genuvah"]
    assert parts == Parser().parse(word).flat()


def test_yissachar():
    """yissachar often lacks one of the sin dots"""
    word = r"יִשָּׂשכָר‎"  # yi-sa-khar
    parts = [
        "yod",
        "hiriq",
        "sin",
        "dagesh-hazaq",
        "qamats-gadol",
        "sin",
        "khaf",
        "qamats",
        "resh",
    ]
    assert parts == Parser().parse(word).flat()


def test_mitzvot_matzot():
    """Mitzvot can be spelled several ways (not to be confused with matzot)."""
    zwnj = r"מִצְו‌ֹת‎"  # mitz-voth
    haser_for_vav = r"מִצְוֺת‎"  # mitz-voth
    precomposed = r"מִצְוֹת"  # mitz-voth
    matzot = r"מַצּוֹת‎"  # ma-tzot

    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser().parse(zwnj).flat()
    assert parts == Parser().parse(haser_for_vav).flat()
    assert parts == Parser().parse(precomposed).flat()

    parts = ["mem", "patah", "tsadi", "dagesh-hazaq", "holam-male-vav", "sav"]
    assert parts == Parser().parse(matzot).flat()
