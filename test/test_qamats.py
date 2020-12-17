#!/usr/bin/python
"""`qamats`, `qamats-gadol`, `qamats-qatan`"""

# pkg
from hebphonics.grammar import Parser

## `qamats-gadol`


def test_qamats_gadol_dagesh_hazaq():
    """`qamats` under `dagesh-hazaq` is `qamats-gadol` (qamats-gadol-dagesh-hazaq)"""
    word = r"הַגָּן"  # ha-gan (Genesis 2:9)
    parts = ["he", "patah", "gimel", "dagesh-hazaq", "qamats-gadol", "nun-sofit"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_yod_glide():
    """`qamats` before `yod-glide` is `qamats-gadol` (qamats-gadol-yod-glide)"""
    word = r"חָי"  # hai (Genesis 3:20)
    parts = ["het", "qamats-gadol", "yod-glide"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_mapiq_he():
    """`qamats` before `mapiq-he` is `qamats-gadol` (qamats-gadol-mapiq-he)"""
    word = r"בָהּ"  # vah
    parts = ["vet", "qamats-gadol", "mapiq-he", "mapiq"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_eim_qria():
    """`qamats` before `eim-qria` is `qamats-gadol` (qamats-gadol-eim-qria)"""
    word = r"נָא"  # na (qamats)
    parts = ["nun", "qamats-gadol", "eim-qria-alef"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_vowel():
    """`qamats` before a vowel (or is final vowel) is `qamats-gadol` (qamats-gadol-vowel)"""
    word = r"עָקֵב"  # a-kei (Genesis 3:15)
    parts = ["ayin", "qamats-gadol", "qof", "tsere", "vet"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_meteg():
    """`qamats` with `meteg` is `qamats-gadol` (qamats-gadol-meteg)"""
    word = r"בָּֽם"  # bam (Leviticus 11:43)
    parts = ["bet", "dagesh-qal", "qamats-gadol", "mem-sofit"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_accent():
    """`qamats` with accent is `qamats-gadol` (qamats-gadol-accent)"""
    word = r"נָ֤ע"  # na (Genesis 4:14)
    parts = ["nun", "qamats-gadol", "ayin"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_next_accent():
    """`qamats` with first accent on syllable is `qamats-gadol` (qamats-gadol-next-accent)"""
    word = r"אָז֩"  # az (Leviticus 26:34)
    parts = ["alef", "qamats-gadol", "zayin"]
    assert parts == Parser().parse(word).flat()


def test_qamats_gadol_before_sheva_na():
    """`qamats` before `sheva-na` without `dagesh` is `qamats-gadol` (qamats-gadol-before-sheva-na)"""
    word = r"יָרְאוּ"  # ya-re-u (Exodus 1:21)
    parts = ["yod", "qamats-gadol", "resh", "sheva-na", "alef", "shuruq"]
    assert parts == Parser().parse(word).flat()


## `qamats-qatan`


def test_qamats_qatan_unicode():
    """`POINT_QAMATS_QATAN` is `qamats-qatan`"""
    word = r"כׇּל"  # kol (synthetic)
    parts = ["kaf", "dagesh-qal", "qamats-qatan", "lamed"]
    assert parts == Parser().parse(word).flat()


def test_qamats_qatan_maqaf():
    """`qamats` in closed syllable in non-last word with `maqaf` is `qamats-qatan`"""
    word = r"מָר־"  # mor (Exodus 30:23)
    parts = ["mem", "qamats-qatan", "resh"]
    assert parts == Parser().parse(word).flat()


def test_qamatas_qatan_closed_unaccented():
    """`qamats` in an unaccented, closed syllable is `qamats-qatan` (qamats-qatan-closed-unaccented)"""
    word = r"וַיָּ֨מָת"  # va-yamot (Deuteronomy 34:5)
    parts = [
        "vav",
        "patah",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
        "mem",
        "qamats-qatan",
        "sav",
    ]
    assert parts == Parser().parse(word).flat()


def test_qamatas_gadol_telish_gedola():
    """`qamats` in word with `telisha-gedola` is `qamats-gadol`"""
    word = r"הַ֠גָּמָל"  # ha-ga-mal (Leviticus 11:4)
    parts = [
        "he",
        "patah",
        "gimel",
        "dagesh-hazaq",
        "qamats-gadol",
        "mem",
        "qamats-gadol",
        "lamed",
    ]
    assert parts == Parser().parse(word).flat()


def test_qamats_qatan_next_accent():
    """`qamats` in closed syllable with non-first accent is `qamats-qatan`"""
    word = r"וַיָּ֩שָׁב֩"  # va-ya-shov (Genesis 33:16)
    parts = [
        "vav",
        "patah",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
        "shin",
        "qamats-qatan",
        "vet",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"וַיָּ֨רָץ֙"  # va-ya-rotz (Numbers 17:12)
    parts = [
        "vav",
        "patah",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
        "resh",
        "qamats-qatan",
        "tsadi-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_qamats_qatan_before_sheva_nah():
    """`qamats` before `sheva-nah` is `qamats-qatan`"""
    word = r"מְלָךְ"  # me-lokh (Genesis 36:31)
    parts = ["mem", "sheva-na", "lamed", "qamats-qatan", "khaf-sofit", "sheva-nah"]
    assert parts == Parser().parse(word).flat()


def test_qamats_before_midword_sheva_not_vav():
    """`qamats` before midword `vav` with `sheva-nah` is NOT `qamats-qatan`"""
    word = r"לַשָּֽׁוְא"  # la-shav (Deuteronomy 5:11; needs `meteg`)
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


def test_qamats_qatan_unstresssed_closed():
    """`qamats` in unstressed closed syllable is `qamats-qatan`"""
    word = r"וַיָּ֥קָם"
    parts = [
        "vav",
        "patah",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
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
        "qamats-gadol",
        "mapiq-he",
        "mapiq",
    ]
    assert parts == Parser().parse(word).flat()


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


def test_qamats_qatan_dagesh_sheva():
    """`qamats` before `dagesh` with `sheva` is `qamats-qatan`"""
    word = r"בְעָזְּךָ"
    parts = [
        "vet",
        "sheva-na",
        "ayin",
        "qamats-qatan",
        "zayin",
        "dagesh-hazaq",
        "sheva-na",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()


def test_qamats_yod_vav():
    """`qamats` followed by bare `yod` and `vav` is `qamats-yod-vav`"""
    word = r"אֵלָיו"  # ei-lav
    parts = ["alef", "tsere", "lamed", "qamats-gadol", "yod-glide", "vav"]
    assert parts == Parser().parse(word).flat()
