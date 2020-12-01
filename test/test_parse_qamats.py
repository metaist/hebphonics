#!/usr/bin/python
"""`qamats`, `qamats-gadol`, `qamats-qatan`"""

# pkg
from hebphonics.grammar import Parser


def test_unicode_qamats_qatan():
    """`POINT_QAMATS_QATAN` is `qamats-qatan`"""
    word = r"כׇּל"  # kol
    parts = ["kaf", "dagesh-qal", "qamats-qatan", "lamed"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_meteg():
    """`qamats` with `meteg` is `qamats-gadol`"""
    word = r"הָאָֽרֶץ"  # ha-a-rets
    parts = [
        "he",
        "qamats-gadol",
        "alef",
        "qamats-gadol",
        "resh",
        "segol",
        "tsadi-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_accent():
    """`qamats` with accent is `qamats-gadol`"""
    word = r"וַיָּ֥שֶׂם"  # va-ya-sem
    parts = [
        "vav",
        "patah",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
        "sin",
        "segol",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()


# def test_qamats_qatan_before_midword_sheva_nah():
#     """`qamats` before `sheva-nah` is `qamats-qatan`"""
#     word = r"אָזְנְךָ"  # oz-ne-ha
#     parts = [
#         "alef",
#         "qamats-qatan",
#         "zayin",
#         "sheva-nah",
#         "nun",
#         "sheva-na",
#         "khaf-sofit",
#         "qamats",
#     ]
#     assert parts == Parser().parse(word).flat()


def test_qamats_before_midword_sheva_not_vav():
    """`qamats` before midword `vav` with `sheva-nah` is NOT `qamats-qatan`"""
    word = r"לַשָּׁוְא"
    parts = [
        "lamed",
        "patah",
        "shin",
        "dagesh-hazaq",
        "qamats-gadol",
        "vav",
        "sheva-nah",
        "alef",
    ]
    assert parts == Parser().parse(word).flat()


def TODO_test_qamats_qatan_unstresssed_closed():
    """H501: `qamats` in unstressed closed syllable is `qamats-qatan` (qq-unstressed-closed)"""
    word = r"וַיָּקָם"
    parts = [
        "vav",
        "patah",
        "yod",
        "dagesh-hazaq",
        "qamats",
        "qof",
        "qamats-qatan",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"רָחְבָּהּ"
    parts = [
        "resh",
        "qamats-qatan",
        "het",
        "sheva-nah",
        "bet",
        "dagesh-qal",
        "qamats-male-he",
        "mapiq-he",
        "mapiq",
    ]
    assert parts == Parser().parse(word).flat()


# def test_qamats_qatan_maqaf():
#     """H502: `qamats` in non-last word with `maqaf` is `qamats-qatan` (qq-maqaf)"""
#     word = r"כָּל־"
#     parts = ["kaf", "dagesh-qal", "qamats-qatan", "lamed"]
#     assert parts == Parser().parse(word).flat()


# def test_qamats_qatan_before_hataf_qamats():
#     """H503: `qamats` before `hataf-qamats` is `qamats-qatan` (qq-hataf-qamats)"""
#     word = r"בַּצָּהֳרָיִם"
#     parts = [
#         "bet",
#         "dagesh-qal",
#         "patah",
#         "tsadi",
#         "dagesh-hazaq",
#         "qamats-qatan",
#         "he",
#         "hataf-qamats",
#         "resh",
#         "qamats-gadol",
#         "yod",
#         "hiriq",
#         "mem-sofit",
#     ]
#     assert parts == Parser().parse(word).flat()


def TODO_test_qamats_qatan_after_be_le_prefix():
    """H504: `qamats` in unstressed syllable after `be|le`-prefix is `qamtas-qatan` (qq-be-le-prefix)"""
    word = r"בְּחָכְמָה"
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "het",
        "qamats-qatan",
        "khaf",
        "sheva-na",
        "mem",
        "qamats-male-he",
        "he",
    ]
    assert parts == Parser().parse(word).flat()
