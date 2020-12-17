#!/usr/bin/python
"""`eim-qria-`, `shuruq`, `holam-male`"""

# pkg
from hebphonics.grammar import Parser


def test_vav_holam_haser_for_vav():
    """`HOLAM_HASER_FOR_VAV` is `holam-haser`"""
    word = r"מִצְוֺת‎"  # mi-ts-voth
    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser().parse(word).flat()


def test_shuruq_at_start():
    """`shuruq` at the start of a word (eim-qria-vav-is-shuruq-start)"""
    word = r"וּבֶן"  # u-ven
    parts = ["shuruq", "vet", "segol", "nun-sofit"]
    assert parts == Parser().parse(word).flat()


def test_vav_is_shuruq():
    """`vav` with `dagesh` NOT after vowel is `shuruq` (eim-qria-vav-is-shuruq-middle)"""
    word = r"תֹהוּ"  # to-hu
    parts = ["sav", "holam-haser", "he", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_vav_is_holam_male():
    """`vav`, `holam` NOT after vowel or sheva is `holam-male` (eim-qria-vav-is-holam-male)"""
    word = r"אוֹר"  # or
    parts = ["alef", "holam-male-vav", "resh"]
    assert parts == Parser().parse(word).flat()

    word = r"בּוֹא"  # bo
    parts = ["bet", "dagesh-qal", "holam-male-vav", "alef"]
    assert parts == Parser().parse(word).flat()


def test_vav_holam_after_vowel():
    """`vav` with `holam_haser` after vowel or sheva `vav`, `holam-haser` (!eim-qria-vav-is-holam-male)"""
    word = r"עֲוֺן"  # a-von
    parts = ["ayin", "hataf-patah", "vav", "holam-haser", "nun-sofit"]
    assert parts == Parser().parse(word).flat()

    word = r"מִצְוֺת"  # mits-voth
    parts = ["mem", "hiriq", "tsadi", "sheva-nah", "vav", "holam-haser", "sav"]
    assert parts == Parser().parse(word).flat()


def test_vav_dagesh_hazaq():
    """`vav` with `dagesh` after/has vowel is `vav`, `dagesh-hazaq` (dagesh-hazaq-default)"""
    word = r"חַוָּה"  # cha-vah
    parts = ["het", "patah", "vav", "dagesh-hazaq", "qamats-gadol", "eim-qria-he"]
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


def test_hiriq_male():
    """`hiriq` before bare `yod` is `hiriq-male` (eim-qria-yod-is-hiriq-male)"""
    word = r"כִּי"
    parts = ["kaf", "dagesh-qal", "hiriq-male-yod", "eim-qria-yod"]
    assert parts == Parser().parse(word).flat()


def test_eim_qria_alef():
    """bare `alef` after `qamats|patah|segol|tsere|holam|shuruq` is `eim-qria-alef` (eim-qria-alef)"""
    word = r"נָא"  # na (qamats)
    parts = ["nun", "qamats-gadol", "eim-qria-alef"]
    assert parts == Parser().parse(word).flat()

    word = r"חַטַּאת"  # ha-tat (patah)
    parts = ["het", "patah", "tet", "dagesh-hazaq", "patah", "eim-qria-alef", "sav"]
    assert parts == Parser().parse(word).flat()

    word = r"יֵרֶא"  # ya-re (segol)
    parts = ["yod", "tsere", "resh", "segol", "eim-qria-alef"]
    assert parts == Parser().parse(word).flat()

    word = r"צֵא"  # tsei (tsere)
    parts = ["tsadi", "tsere", "eim-qria-alef"]
    assert parts == Parser().parse(word).flat()

    word = r"בֹּא"  # bo (holam)
    parts = ["bet", "dagesh-qal", "holam-haser", "eim-qria-alef"]
    assert parts == Parser().parse(word).flat()

    word = r"הוּא"  # hu (shuruq)
    parts = ["he", "shuruq", "eim-qria-alef"]
    assert parts == Parser().parse(word).flat()


def test_eim_qria_he():
    """bare `he` after `qamats|patah|segol|tsere|holam` is `eim-qria-he` (eim-qria-he)"""
    word = r"מָה"  # mah (qamats)
    parts = ["mem", "qamats-gadol", "eim-qria-he"]
    assert parts == Parser().parse(word).flat()

    word = r"מַה"  # mah (patah)
    parts = ["mem", "patah", "eim-qria-he"]
    assert parts == Parser().parse(word).flat()

    word = r"מֶה"  # meh (segol)
    parts = ["mem", "segol", "eim-qria-he"]
    assert parts == Parser().parse(word).flat()

    word = r"שֵׂה"  # sei (tsere)
    parts = ["sin", "tsere", "eim-qria-he"]
    assert parts == Parser().parse(word).flat()

    word = r"אֵיפֹה"  # ei-foh (holam)
    parts = ["alef", "tsere", "eim-qria-yod", "fe", "holam-haser", "eim-qria-he"]
    assert parts == Parser().parse(word).flat()


def test_eim_qria_yod():
    """bare `yod` after `hiriq|tsere|segol` is `eim-qria-yod` (eim-qria-yod)"""
    # NOTE: `yod` after `hiriq` is already `hiriq-male`

    word = r"אֵין"  # ein (tsere)
    parts = ["alef", "tsere", "eim-qria-yod", "nun-sofit"]
    assert parts == Parser().parse(word).flat()

    word = r"אֵלֶיךָ"  # ei-lecha (segol)
    parts = [
        "alef",
        "tsere",
        "lamed",
        "segol",
        "eim-qria-yod",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()
