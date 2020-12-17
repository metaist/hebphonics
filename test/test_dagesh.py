#!/usr/bin/python
"""`dagesh-`, `mapiq-`"""

# pkg
from hebphonics.grammar import Parser


def test_mapiq_alef():
    """`dagesh` in `alef` is `mapiq-alef` (dagesh-is-mapiq-alef)"""
    word = r"רֻאּֽוּ"  # roo'oo (Job 33:21)
    parts = ["resh", "qubuts", "mapiq-alef", "mapiq", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_mapiq_he():
    """`dagesh` in **last** `he` is `mapiq-he` (dagesh-is-mapiq-he)"""
    word = r"בָּהּ"  # bah (Genesis 21:23)
    parts = ["bet", "dagesh-qal", "qamats-gadol", "mapiq-he", "mapiq"]
    assert parts == Parser().parse(word).flat()


def test_he_dagesh_hazaq():
    """`dagesh` in non-last `he` is **non-standard** `dagesh-hazaq` (dagesh-in-guttural)"""
    word = r"חֲמֹרֵיהֶּם"  # cha-mo-rei-hem (non-standard)
    parts = [
        "het",
        "hataf-patah",
        "mem",
        "holam-haser",
        "resh",
        "tsere",
        "eim-qria-yod",
        "he",
        "dagesh-hazaq",
        "segol",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_dagesh_none_bgdkft():
    """BGDKFT letter _without_ dagesh has a different name (dagesh-none-bgdkft)"""
    word = r"אֶת"
    parts = ["alef", "segol", "sav"]
    assert parts == Parser().parse(word).flat()


def test_bgdkft_after_vowel():
    """`dagesh` in BGDKFT after vowel is `dagesh-hazaq` (dagesh-hazaq-bgdkft)"""
    word = r"שַׁבָּת"  # sha-bbath
    parts = ["shin", "patah", "bet", "dagesh-hazaq", "qamats-gadol", "sav"]
    assert parts == Parser().parse(word).flat()


def test_bgdkft_not_after_vowel():
    """`dagesh` in BGDKFT NOT after vowel is `dagesh-qal` (dagesh-qal-bgdkf)"""
    word = r"בָּרָא"  # ba-ra
    parts = [
        "bet",
        "dagesh-qal",
        "qamats-gadol",
        "resh",
        "qamats-gadol",
        "eim-qria-alef",
    ]
    assert parts == Parser().parse(word).flat()

    word = "דָּבָר"  # da-var
    parts = ["dalet", "dagesh-qal", "qamats-gadol", "vet", "qamats", "resh"]
    assert parts == Parser().parse(word).flat()

    word = "פֶּה"  # poh
    parts = ["pe", "dagesh-qal", "segol", "eim-qria-he"]
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
    assert parts == Parser().parse(word).flat()


def test_dagesh_hazaq_default():
    """default `dagesh` is `dagesh-hazaq` (dagesh-hazaq-default)"""
    word = r"הַמַּיִם"  # ha-ma-yim
    parts = [
        "he",
        "patah",
        "mem",
        "dagesh-hazaq",
        "patah",
        "yod-glide",
        "hiriq",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()
