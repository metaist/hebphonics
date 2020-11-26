#!/usr/bin/python
"""`male-`"""

# pkg
from hebphonics.grammar import Parser


def test_hiriq_male():
    """H301: `hiriq` before bare `yod` is `hiriq-male` (male-hiriq)"""
    word = r"כִּי"
    parts = ["kaf", "dagesh-qal", "hiriq-male-yod", "yod"]
    assert parts == Parser().parse(word).flat()


def test_tsere_male():
    """H302: `tsere` before bare `alef|he|yod` is `tsere-male` (male-tsere)"""
    word = r"צֵאת"
    parts = ["tsadi", "tsere-male-alef", "alef", "sav"]
    assert parts == Parser().parse(word).flat()

    word = r"עֲשֵׂה"
    parts = ["ayin", "hataf-patah", "sin", "tsere-male-he", "he"]
    assert parts == Parser().parse(word).flat()

    word = r"בֵּין"
    parts = ["bet", "dagesh-qal", "tsere-male-yod", "yod", "nun-sofit"]
    assert parts == Parser().parse(word).flat()


def test_segol_male():
    """H303: `segol` before bare `alef|he|yod` is `segol-male` (male-segol)"""
    word = r"וַתֵּרֶא"
    parts = [
        "vav",
        "patah",
        "tav",
        "dagesh-hazaq",
        "tsere",
        "resh",
        "segol-male-alef",
        "alef",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"תַּעֲשֶׂה"
    parts = [
        "tav",
        "dagesh-qal",
        "patah",
        "ayin",
        "hataf-patah",
        "sin",
        "segol-male-he",
        "he",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"עֶגְלֵי"
    parts = ["ayin", "segol", "gimel", "sheva-nah", "lamed", "tsere-male-yod", "yod"]
    assert parts == Parser().parse(word).flat()


def test_patah_male():
    """H304: `patah` before bare `alef|he` is `patah-male` (male-patah)"""
    word = r"לִקְרַאת"
    parts = [
        "lamed",
        "hiriq",
        "qof",
        "sheva-nah",
        "resh",
        "patah-male-alef",
        "alef",
        "sav",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"מַה"
    parts = ["mem", "patah-male-he", "he"]
    assert parts == Parser().parse(word).flat()


def test_qamats_male():
    """`qamats` before bare `alef|he` is `qamats-male` (qamats-male)"""
    word = r"קָרָא"  # ka-ra
    parts = ["qof", "qamats-gadol", "resh", "qamats-male-alef", "alef"]
    assert parts == Parser().parse(word).flat()

    word = r"שָׁנָה"  # sha-na
    parts = ["shin", "qamats-gadol", "nun", "qamats-male-he", "he"]
    assert parts == Parser().parse(word).flat()


def test_holam_male():
    """H306: `holam` before bare `alef|he` is `holam-male` (male-holam)"""
    word = "צֹאנְךָ"
    parts = [
        "tsadi",
        "holam-male-alef",
        "alef",
        "nun",
        "sheva-na",
        "khaf-sofit",
        "qamats",
    ]
    assert parts == Parser().parse(word).flat()
