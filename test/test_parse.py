#!/usr/bin/env python
# coding: utf-8
"""Test Hebrew grammar parsing."""

# pkg
from hebphonics.grammar import Parser


def test_empty():
    """Parse an empty string."""
    assert Parser("").parse() == []


## H1xx: `mapiq-` and `dagesh-` ##


def test_mapiq_alef():
    """H101: `dagesh` in `alef` is `mapiq-alef` (dagesh-mapiq-alef)"""
    word = r"רֻאּֽוּ"
    parts = ["resh", "qubuts", "mapiq-alef", "mapiq", "shuruq"]
    assert parts == Parser(word).parse()


def test_mapiq_he():
    """H102: `dagesh` in last `he` is `mapiq-he` (dagesh-mapiq-he)"""
    word = r"בָּהּ"
    parts = ["bet", "dagesh-qal", "qamats", "mapiq-he", "mapiq"]
    assert parts == Parser(word).parse()


def test_he_dagesh_hazaq():
    """H103: `dagesh` in non-last `he` is `dagesh-hazaq` (dagesh-hazaq-he)"""
    word = r"חֲמֹרֵיהֶּם"
    parts = [
        "het",
        "hataf-patah",
        "mem",
        "holam-haser",
        "resh",
        "tsere-male",
        "yod",
        "he",
        "dagesh-hazaq",
        "segol",
        "mem-sofit",
    ]
    assert parts == Parser(word).parse()


def test_bgdkft_after_vowel():
    """H104: `dagesh` in BGDKFT after vowel is `dagesh-hazaq` (dagesh-hazaq-bgdkft)"""
    word = r"שַׁבָּת"
    parts = ["shin", "patah", "bet", "dagesh-hazaq", "qamats", "sav"]
    assert parts == Parser(word).parse()


def test_bgdkft_not_after_vowel():
    """H105: `dagesh` in BGDKFT NOT after vowel is `dagesh-qal` (dagesh-qal-bgdkft)"""
    word = r"בָּרָא"
    parts = ["bet", "dagesh-qal", "qamats", "resh", "qamats-male", "alef"]
    assert parts == Parser(word).parse()

    word = "דָּבָר"
    parts = ["dalet", "dagesh-qal", "qamats", "vet", "qamats", "resh"]
    assert parts == Parser(word).parse()

    word = "פֶּה"
    parts = ["pe", "dagesh-qal", "segol-male", "he"]
    assert parts == Parser(word).parse()

    word = "מִדְבָּר"
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
    assert parts == Parser(word).parse()


def test_other_dagesh():
    """H106: any other `dagesh` is a `dagesh-hazaq` (dagesh-hazaq-other)"""
    word = r"הַמַּיִם"
    parts = ["he", "patah", "mem", "dagesh-hazaq", "patah", "yod", "hiriq", "mem-sofit"]
    assert parts == Parser(word).parse()


## H2xx: `sheva-` ##


def test_sheva_na_start():
    """H201: `sheva` at word start is `sheva-na` (sheva-na-word-start)"""
    word = r"וְאֵת"
    parts = ["vav", "sheva-na", "alef", "tsere", "sav"]
    assert parts == Parser(word).parse()

    word = r"קְדוֹשׁ"
    parts = ["qof", "sheva-na", "dalet", "holam-male", "shin"]
    assert parts == Parser(word).parse()

    word = r"בְּלִי"
    parts = ["bet", "dagesh-qal", "sheva-na", "lamed", "hiriq-male", "yod"]
    assert parts == Parser(word).parse()


def test_sheva_nah_end():
    """H202: `sheva` at the end of a word is `sheva-nah` (sheva-nah-word-end)"""
    word = r"הַחֹשֶׁךְ"
    parts = [
        "he",
        "patah",
        "het",
        "holam-haser",
        "shin",
        "segol",
        "khaf-sofit",
        "sheva-nah",
    ]
    assert parts == Parser(word).parse()


def test_sheva_na_under_dagesh_hazaq():
    """H203: `sheva` under `dagesh-hazaq` is `sheva-na` (sheva-na-dagesh-hazaq)"""
    word = r"הַמְּאֹרֹת"
    parts = [
        "he",
        "patah",
        "mem",
        "dagesh-hazaq",
        "sheva-na",
        "alef",
        "holam-haser",
        "resh",
        "holam-haser",
        "sav",
    ]
    assert parts == Parser(word).parse()


def test_sheva_na_after_long_vowel():
    """H204: `sheva` after long vowel is `sheva-na` (sheva-na-after-long-vowel)"""
    word = r"הָיְתָה"
    parts = ["he", "qamats", "yod", "sheva-na", "sav", "qamats-male", "he"]
    assert parts == Parser(word).parse()


def test_sheva_na_after_holam_alef():
    """H204: `sheva` after long vowel is `sheva-na` (sheva-na-after-long-vowel)
    (including holam+alef)
    """
    word = r"תֹּאמְרוּ"
    parts = [
        "tav",
        "dagesh-qal",
        "holam-male",
        "alef",
        "mem",
        "sheva-na",
        "resh",
        "shuruq",
    ]
    assert parts == Parser(word).parse()


def test_sheva_nah_after_short_vowel():
    """H205: `sheva` after short vowel is `sheva-nah` (sheva-nah-after-short-vowel)"""
    word = r"פַּרְעֹה"
    parts = [
        "pe",
        "dagesh-qal",
        "patah",
        "resh",
        "sheva-nah",
        "ayin",
        "holam-male",
        "he",
    ]
    assert parts == Parser(word).parse()

    word = r"נֶאֱסְפוּ"
    parts = [
        "nun",
        "segol",
        "alef",
        "hataf-segol",
        "samekh",
        "sheva-nah",
        "fe",
        "shuruq",
    ]
    assert parts == Parser(word).parse()


def test_sheva_nah_alef_end():
    """H206: `sheva` before last bare `alef` is `sheva-nah` (sheva-nah-alef-end)"""
    word = "חֵטְא"
    parts = ["het", "tsere", "tet", "sheva-nah", "alef"]
    assert parts == Parser(word).parse()


def test_sheva_na_before_same_sounding_letter():
    """H207: `sheva` before same letter is `sheva-na` (sheva-na-double-letter)"""
    word = r"הַלְלוּ"
    parts = ["he", "patah", "lamed", "sheva-na", "lamed", "shuruq"]
    assert parts == Parser(word).parse()


def test_double_sheva_middle():
    """H208: two `sheva` midword are `sheva-nah`, `sheva-na` (sheva-double-midword)"""
    word = r"עֶזְרְךָ"
    parts = [
        "ayin",
        "segol",
        "zayin",
        "sheva-nah",
        "resh",
        "sheva-na",
        "khaf-sofit",
        "qamats",
    ]
    assert parts == Parser(word).parse()


def test_double_sheva_end():
    """H209: two `sheva` at word end are `sheva-na`, `sheva-na` (sheva-double-end)"""
    word = r"וְיֵשְׁתְּ"
    parts = [
        "vav",
        "sheva-na",
        "yod",
        "tsere",
        "shin",
        "sheva-na",
        "tav",
        "dagesh-qal",
        "sheva-na",
    ]
    assert parts == Parser(word).parse()


def test_not_real_sheva():
    """an unknown kind of sheva"""
    word = r"זרְע"
    parts = ["zayin", "resh", "sheva", "ayin"]
    assert parts == Parser(word).parse()


## H3xx: `-male` ##


def test_hiriq_male():
    """H301: `hiriq` before bare `yod` is `hiriq-male` (male-hiriq)"""
    word = r"כִּי"
    parts = ["kaf", "dagesh-qal", "hiriq-male", "yod"]
    assert parts == Parser(word).parse()


def test_tsere_male():
    """H302: `tsere` before bare `alef|he|yod` is `tsere-male` (male-tsere)"""
    word = r"צֵאת"
    parts = ["tsadi", "tsere-male", "alef", "sav"]
    assert parts == Parser(word).parse()

    word = r"עֲשֵׂה"
    parts = ["ayin", "hataf-patah", "sin", "tsere-male", "he"]
    assert parts == Parser(word).parse()

    word = r"בֵּין"
    parts = ["bet", "dagesh-qal", "tsere-male", "yod", "nun-sofit"]
    assert parts == Parser(word).parse()


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
        "segol-male",
        "alef",
    ]
    assert parts == Parser(word).parse()

    word = r"תַּעֲשֶׂה"
    parts = [
        "tav",
        "dagesh-qal",
        "patah",
        "ayin",
        "hataf-patah",
        "sin",
        "segol-male",
        "he",
    ]
    assert parts == Parser(word).parse()

    word = r"עֶגְלֵי"
    parts = ["ayin", "segol", "gimel", "sheva-nah", "lamed", "tsere-male", "yod"]
    assert parts == Parser(word).parse()


def test_patah_male():
    """H304: `patah` before bare `alef|he` is `patah-male` (male-patah)"""
    word = r"לִקְרַאת"
    parts = ["lamed", "hiriq", "qof", "sheva-nah", "resh", "patah-male", "alef", "sav"]
    assert parts == Parser(word).parse()

    word = r"מַה"
    parts = ["mem", "patah-male", "he"]
    assert parts == Parser(word).parse()


def test_qamats_male():
    """H305: `qamats` before bare `alef|he` is `qamats-male` (male-qamats)"""
    word = r"קָרָא"
    parts = ["qof", "qamats", "resh", "qamats-male", "alef"]
    assert parts == Parser(word).parse()

    word = r"שָׁנָה"
    parts = ["shin", "qamats", "nun", "qamats-male", "he"]
    assert parts == Parser(word).parse()


def test_holam_male():
    """H306: `holam` before bare `alef|he` is `holam-male` (male-holam)"""
    word = "צֹאנְךָ"
    parts = ["tsadi", "holam-male", "alef", "nun", "sheva-na", "khaf-sofit", "qamats"]
    assert parts == Parser(word).parse()


## H4xx: `patah-genuvah` ##


def test_patah_genuvah():
    """H401: `patah` on last `het|ayin|mapiq-he` is `patah-genuvah` (patah-genuvah)"""
    word = r"נֹחַ"
    parts = ["nun", "holam-haser", "het", "patah-genuvah"]
    assert parts == Parser(word).parse()


## H5xx: `qamats-qatan` ##


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
    assert parts == Parser(word).parse()


def test_qamats_qatan_maqaf():
    """H502: `qamats` in non-last word with `maqaf` is `qamats-qatan` (qq-maqaf)"""
    word = r"כָּל־"
    parts = ["kaf", "dagesh-qal", "qamats-qatan", "lamed"]
    assert parts == Parser(word).parse()


def test_qamats_qatan_before_hataf_qamats():
    """H503: `qamats` before `hataf-qamats` is `qamats-qatan` (qq-hataf-qamats)"""
    word = r"בַּצָּהֳרָיִם"
    parts = [
        "bet",
        "dagesh-qal",
        "patah",
        "tsadi",
        "dagesh-hazaq",
        "qamats-qatan",
        "he",
        "hataf-qamats",
        "resh",
        "qamats",
        "yod",
        "hiriq",
        "mem-sofit",
    ]
    assert parts == Parser(word).parse()


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
        "qamats-male",
        "he",
    ]
    assert parts == Parser(word).parse()


## H6xx: `vav` ##


def test_vav_holam_haser_for_vav():
    """H601: `VAV` followed by `HOLAM_HASER_FOR_VAV` is `vav`, `holam-haser` (vav-holam-haser-unicode)"""
    word = r"מִצְוֺת‎"
    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser(word).parse()


def test_vav_is_holam_male():
    """H602: `vav`, `HOLAM_HASER` NOT after vowel or sheva is `holam-male` (vav-is-holam-male)"""
    word = r"אוֹר"
    parts = ["alef", "holam-male", "resh"]
    assert parts == Parser(word).parse()


def test_vav_holam_after_vowel():
    """H603: `VAV` with `HOLAM_HASER` after vowel or sheva `vav`, `holam-haser` (vav-holam-haser)"""
    word = r"עֲוֺן"
    parts = ["ayin", "hataf-patah", "vav", "holam-haser", "nun-sofit"]
    assert parts == Parser(word).parse()

    word = r"מִצְוֺת"
    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser(word).parse()


def test_vav_is_shuruq():
    """H604: `VAV` with `DAGESH` NOT after vowel is `shuruq` (vav-is-shurug)"""
    word = r"תֹהוּ"
    parts = ["sav", "holam-haser", "he", "shuruq"]
    assert parts == Parser(word).parse()


def test_vav_dagesh_hazaq():
    """H605: `VAV` with `DAGESH` after/has vowel is `vav`, `dagesh-hazaq` (vav-dagesh-hazaq)"""
    word = r"חַוָּה"
    parts = ["het", "patah", "vav", "dagesh-hazaq", "qamats-male", "he"]
    assert parts == Parser(word).parse()

    word = r"וְיִשְׁתַּחֲוּוּ"
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
    assert parts == Parser(word).parse()


## Other Words ##


def test_no_rules():
    """a word that doesn't require any special rules"""
    word = "אֵת"
    parts = ["alef", "tsere", "sav"]
    assert parts == Parser(word).parse()


def test_yissachar():
    """yissachar often lacks one of the sin dots"""
    word = "יִשָּׂשכָר‎"
    parts = [
        "yod",
        "hiriq",
        "sin",
        "dagesh-hazaq",
        "qamats",
        "sin",
        "khaf",
        "qamats",
        "resh",
    ]
    assert parts == Parser(word).parse()


def test_mitzvot_matzot():
    """Mitzvot can be spelled several ways (not to be confused with matzot)."""
    zwnj = "מִצְו‌ֹת‎"
    haser_for_vav = "מִצְוֺת‎"
    precomposed = "מִצְוֹת‎"
    matzot = "מַצּוֹת‎"

    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser(zwnj).parse()
    assert parts == Parser(haser_for_vav).parse()
    assert parts == Parser(precomposed).parse()

    parts = ["mem", "patah", "tsadi", "dagesh-hazaq", "holam-male", "sav"]
    assert parts == Parser(matzot).parse()
