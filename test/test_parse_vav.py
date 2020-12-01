#!/usr/bin/python
"""`vav`"""

# pkg
from hebphonics.grammar import Parser


def test_vav_holam_haser_for_vav():
    """`HOLAM_HASER_FOR_VAV` is `holam-haser`"""
    word = r"מִצְוֺת‎"  # mi-ts-voth
    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser().parse(word).flat()


def test_shuruq_at_start():
    """`shuruq` at the start of a word (shuruq-start)"""
    word = r"וּבֶן"  # u-ven
    parts = ["shuruq", "vet", "segol", "nun-sofit"]
    assert parts == Parser().parse(word).flat()


def test_vav_is_shuruq():
    """`vav` with `dagesh` NOT after vowel is `shuruq` (vav-is-shurug)"""
    word = r"תֹהוּ"  # to-hu
    parts = ["sav", "holam-haser", "he", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_vav_is_holam_male():
    """`vav`, `holam` NOT after vowel or sheva is `holam-male` (vav-is-holam-male)"""
    word = r"אוֹר"  # or
    parts = ["alef", "holam-male-vav", "resh"]
    assert parts == Parser().parse(word).flat()


def test_vav_holam_after_vowel():
    """`vav` with `holam_haser` after vowel or sheva `vav`, `holam-haser` (!vav-is-holam-male)"""
    word = r"עֲוֺן"  # a-von
    parts = ["ayin", "hataf-patah", "vav", "holam-haser", "nun-sofit"]
    assert parts == Parser().parse(word).flat()

    word = r"מִצְוֺת"  # mits-voth
    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser().parse(word).flat()


def test_vav_dagesh_hazaq():
    """`vav` with `dagesh` after/has vowel is `vav`, `dagesh-hazaq` (dagesh-hazaq-default)"""
    word = r"חַוָּה"  # cha-vah
    parts = ["het", "patah", "vav", "dagesh-hazaq", "qamats-male-he", "he"]
    assert parts == Parser().parse(word).flat()

    word = r"וְיִשְׁתַּחֲוּוּ"  # ve-yish-ta-cha-vu
    parts = [
        "vav",
        "sheva-na",
        "yod",
        "hiriq",
        "shin",
        "sheva-nah",
        "tav",
        "dagesh-qal",
        "patah",
        "het",
        "hataf-patah",
        "vav",
        "dagesh-hazaq",
        "shuruq",
    ]
    assert parts == Parser().parse(word).flat()
