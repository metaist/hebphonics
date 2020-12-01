#!/usr/bin/python
"""`dagesh-`, `mapiq-`"""

# pkg
from hebphonics.grammar import Parser

DEFAULT_DISABLE = ["qamats-qatan-closed-unaccented"]


def test_mapiq_alef():
    """`dagesh` in `alef` is `mapiq-alef` (mapiq-alef)"""
    word = r"רֻאּֽוּ"  # roo'oo
    parts = ["resh", "qubuts", "mapiq-alef", "mapiq", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_mapiq_he():
    """`dagesh` in last `he` is `mapiq-he` (mapiq-he)"""
    word = r"בָּהּ"  # bah
    parts = ["bet", "dagesh-qal", "qamats-male-he", "mapiq-he", "mapiq"]
    assert parts == Parser().parse(word).flat()


def test_he_dagesh_hazaq():
    """`dagesh` in non-last `he` is `dagesh-hazaq` (dagesh-hazaq-he)"""
    word = r"חֲמֹרֵיהֶּם"  # cha-mo-rei-hem
    parts = [
        "het",
        "hataf-patah",
        "mem",
        "holam-haser",
        "resh",
        "tsere-male-yod",
        "yod",
        "he",
        "dagesh-hazaq",
        "segol",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_bgdkft_after_vowel():
    """H104: `dagesh` in BGDKFT after vowel is `dagesh-hazaq` (dagesh-hazaq-bgdkft)"""
    word = r"שַׁבָּת"  # sha-bbath
    parts = ["shin", "patah", "bet", "dagesh-hazaq", "qamats", "sav"]
    assert parts == Parser(disabled=DEFAULT_DISABLE).parse(word).flat()


def test_bgdkft_not_after_vowel():
    """H105: `dagesh` in BGDKFT NOT after vowel is `dagesh-qal` (dagesh-qal-bgdkft)"""
    word = r"בָּרָא"  # ba-ra
    parts = ["bet", "dagesh-qal", "qamats-gadol", "resh", "qamats-male-alef", "alef"]
    assert parts == Parser().parse(word).flat()

    word = "דָּבָר"  # da-var
    parts = ["dalet", "dagesh-qal", "qamats-gadol", "vet", "qamats", "resh"]
    assert parts == Parser(disabled=DEFAULT_DISABLE).parse(word).flat()

    word = "פֶּה"  # poh
    parts = ["pe", "dagesh-qal", "segol-male-he", "he"]
    assert parts == Parser().parse(word).flat()

    word = "מִדְבָּר"  # mi-de-bar
    parts = [
        "mem",
        "hiriq",
        "dalet",
        "sheva-nah",
        "bet",
        "dagesh-qal",
        "qamats",
        "resh",
    ]
    assert parts == Parser(disabled=DEFAULT_DISABLE).parse(word).flat()


def test_other_dagesh():
    """H106: any other `dagesh` is a `dagesh-hazaq` (dagesh-hazaq-other)"""
    word = r"הַמַּיִם"  # ha-ma-yim
    parts = ["he", "patah", "mem", "dagesh-hazaq", "patah", "yod", "hiriq", "mem-sofit"]
    assert parts == Parser().parse(word).flat()
