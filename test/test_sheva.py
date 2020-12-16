#!/usr/bin/python
"""`sheva-`"""

# pkg
from hebphonics.grammar import Parser


def test_not_real_sheva():
    """an unknown kind of sheva"""
    word = r"זרְע"  # zra (synthetic)
    parts = ["zayin", "resh", "sheva", "ayin"]
    assert parts == Parser().parse(word).flat()


def test_sheva_gaya():
    """`sheva` with a `meteg` is a `sheva-gaya`"""
    word = "נְֽסָה"  # ne-sah (Psalms 4:7)
    parts = ["nun", "sheva-gaya", "samekh", "qamats-gadol", "eim-qria-he"]
    assert parts == Parser().parse(word).flat()


def test_sheva_merahef():
    """`sheva` before BGDKFT without `dagesh` is `sheva-merahef`"""
    word = r"מַלְכֵי"
    parts = ["mem", "patah", "lamed", "sheva-merahef", "khaf", "tsere", "eim-qria-yod"]
    assert parts == Parser().parse(word).flat()


def test_sheva_merahef_before_sheva():
    """In case of a `sheva-merahef` immediately before another `sheva`, skip"""
    word = r"וְיִפְדְיָה"  # ve-yif-de-ya
    parts = [
        "vav",
        "sheva-na",
        "yod",
        "hiriq",
        "fe",
        "sheva-nah",
        "dalet",
        "sheva-na",
        "yod",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_start():
    """`sheva` at word start is `sheva-na` (sheva-na-start)"""
    word = r"וְאֵת"  # ve-et (Genesis 1:16)
    parts = ["vav", "sheva-na", "alef", "tsere", "sav"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_end():
    """`sheva` at word end is `sheva-nah` (sheva-nah-end)"""
    word = r"לָֽךְ"  # lach (Exodus 33:14)
    parts = ["lamed", "qamats-gadol", "khaf-sofit", "sheva-nah"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_alef_end():
    """`sheva` before last bare `alef` is `sheva-nah` (sheva-nah-alef-end)"""
    word = "חֵטְא"  # cheit (Leviticus 19:17)
    parts = ["het", "tsere", "tet", "sheva-nah", "alef"]
    assert parts == Parser().parse(word).flat()


def test_sheva_double_end():
    """two `sheva` at word end are `sheva-nah`, `sheva-nah` (sheva-double-end)"""
    word = r"אַנְתְּ"  # ahnt
    parts = ["alef", "patah", "nun", "sheva-nah", "tav", "dagesh-qal", "sheva-nah"]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_double_letter():
    """`sheva` before same letter is `sheva-na` (sheva-na-double-letter)"""
    word = r"הַלְלוּ"  # ha-le-lu
    parts = ["he", "patah", "lamed", "sheva-na", "lamed", "shuruq"]
    assert parts == Parser().parse(word).flat()

    word = r"הִנְנִי"  # hi-ne-ni (has vowel under second letter)
    parts = ["he", "hiriq", "nun", "sheva-na", "nun", "hiriq-male-yod", "eim-qria-yod"]
    assert parts == Parser().parse(word).flat()


def test_double_sheva_middle():
    """two `sheva` midword are `sheva-nah`, `sheva-na` (sheva-double-middle)"""
    word = r"יִמְשְׁלוּ"  # yim-she-lu
    parts = ["yod", "hiriq", "mem", "sheva-nah", "shin", "sheva-na", "lamed", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_under_dagesh_hazaq():
    """`sheva` under `dagesh-hazaq` is `sheva-na` (sheva-na-dagesh-hazaq)"""
    word = r"הַבְּאֵר"  # ha-be-eir
    parts = ["he", "patah", "bet", "dagesh-hazaq", "sheva-na", "alef", "tsere", "resh"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_after_shuruq_start():
    """`sheva` after shuruq at word start in non-dagesh letter is `sheva-nah`"""
    word = r"וּרְבוּ"
    parts = ["shuruq", "resh", "sheva-nah", "vet", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_after_short_vowel():
    """`sheva` after short vowel is `sheva-nah` (sheva-nah-after-short-vowel)"""
    word = r"יִשְׁלַח"  # yish-lach
    parts = ["yod", "hiriq", "shin", "sheva-nah", "lamed", "patah", "het"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_after_accent():
    """`sheva` after accent is `sheva-nah` (sheva-nah-after-accent)"""
    word = r"קֵ֑דְמָה"  # keid-ma (Leviticus 16:14)
    parts = ["qof", "tsere", "dalet", "sheva-nah", "mem", "qamats-gadol", "eim-qria-he"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_before_bgdkft_with_dagesh():
    """`sheva` before BGDKFT with `dagesh` is `sheva-nah`"""
    word = r"הָפְכִּי"  # hof-khi
    parts = [
        "he",
        "qamats-qatan",
        "fe",
        "sheva-nah",
        "kaf",
        "dagesh-qal",
        "hiriq-male-yod",
        "eim-qria-yod",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"קָרְבָּן"  # kor-ban
    parts = [
        "qof",
        "qamats-qatan",
        "resh",
        "sheva-nah",
        "bet",
        "dagesh-qal",
        "qamats",  # TODO: should be qamats-gadol
        "nun-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_after_long_vowel():
    """`sheva` after long vowel is `sheva-na` (sheva-na-after-long-vowel)"""
    word = r"יֵשְׁבוּ"  # yei-she-vu
    parts = ["yod", "tsere", "shin", "sheva-na", "vet", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_after_holam_alef():
    """holam + alef is a long vowel (sheva-na-after-long-vowel)"""
    word = r"יֹאמְרוּ"  # yo-me-ru (Exodus 4:1)
    parts = ["yod", "holam-haser", "eim-qria-alef", "mem", "sheva-na", "resh", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_after_initial_vav_with_patah():
    """`sheva` after initial `vav` with `patah` is `sheva-nah` (sheva-nah-after-short-vowel)"""
    word = r"וַיְהִי"  # vay-he (feels weird, but Simanim confirms)
    parts = ["vav", "patah", "yod", "sheva-nah", "he", "hiriq-male-yod", "eim-qria-yod"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_yod_after_he():
    """`sheva` under `yod` with no `dagesh` after `he` is `sheva-nah`"""
    word = r"הַיְאֹר"  # hai-or (Exodus 17:5)
    parts = ["he", "patah", "yod", "sheva-nah", "alef", "holam-haser", "resh"]
    assert parts == Parser().parse(word).flat()


## Wikipedia Tests


def test_sheva_na_wikipedia():
    """examples from <https://en.wikipedia.org/wiki/Shva#Shva_Na>"""

    # first letter of a word
    word = r"מְרַחֵף‎"  # me-ra-chef
    parts = ["mem", "sheva-na", "resh", "patah", "het", "tsere", "fe-sofit"]
    assert parts == Parser().parse(word).flat()

    word = r"לְפָנָי‎"  # le-fa-nai
    parts = [
        "lamed",
        "sheva-na",
        "fe",
        "qamats-gadol",
        "nun",
        "qamats-gadol",
        "yod-glide",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"שְׁמַע‎"  # she-ma
    parts = ["shin", "sheva-na", "mem", "patah", "ayin"]
    assert parts == Parser().parse(word).flat()

    # first of two identical letters
    # no example given

    # second of two shevas under two consecutive letter (except when marked under
    # the last letter of a word)
    word = r"רַעְמְסֵס‎"
    parts = [
        "resh",
        "patah",
        "ayin",
        "sheva-nah",
        "mem",
        "sheva-na",
        "samekh",
        "tsere",
        "samekh",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"וַיִּשְׁמְעוּ"
    parts = [
        "vav",
        "patah",
        "yod-glide",
        "dagesh-hazaq",
        "hiriq",
        "shin",
        "sheva-nah",
        "mem",
        "sheva-na",
        "ayin",
        "shuruq",
    ]
    assert parts == Parser().parse(word).flat()

    # when the letter before the one under which it is marked is marked with a
    # "long" niqqud-variant
    word = r"יְחִֽידְֿךָ‎"  # ye-chi-de-cha
    parts = [
        "yod",
        "sheva-na",
        "het",
        "hiriq-male-yod",
        "eim-qria-yod",
        "dalet",
        "sheva-na",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"הוֹלְכִֿים‎"
    parts = [
        "he",
        "holam-male-vav",
        "lamed",
        "sheva-na",
        "khaf",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"יוֹדְֿעִים‎"
    parts = [
        "yod",
        "holam-male-vav",
        "dalet",
        "sheva-na",
        "ayin",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"מוֹכְֿרִים‎"
    parts = [
        "mem",
        "holam-male-vav",
        "khaf",
        "sheva-na",
        "resh",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    # when marked under a letter with a dagesh ḥazaq
    word = r"מִפְּנֵיכֶם‎"
    parts = [
        "mem",
        "hiriq",
        "pe",
        "dagesh-hazaq",
        "sheva-na",
        "nun",
        "tsere",
        "eim-qria-yod",
        "khaf",
        "segol",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    word = r"מִקְּדָֿשׁ‎"  # mi-ke-dash
    parts = [
        "mem",
        "hiriq",
        "qof",
        "dagesh-hazaq",
        "sheva-na",
        "dalet",
        "qamats",  # TODO: qamats-gadol
        "shin",
    ]
    assert parts == Parser().parse(word).flat()


# Modern Hebrew Sheva <https://en.wikipedia.org/wiki/Shva>
# NOTE: In modern Hebrew, whether a `sheva` is voiced or not does not depend on
# the traditional distinction between `sheva-na` vs `sheva-nah`


def test_modern_sheva_1():
    """`sheva` is voiced when under the first of two letters, both representing the
    same consonant or consonants with identical place and manner of articulation.
    """
    RULE_NAME = "sheva-modern-double-sound"

    word = r"שָׁכְחוּ"  # sha-che-chu (same sound)
    parts = ["shin", "qamats-gadol", "khaf", "sheva-na", "het", "shuruq"]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"מָכְרוּ"  # mach-ru (negative example)
    parts = ["mem", "qamats-gadol", "khaf", "sheva-na", "resh", "shuruq"]
    parsed = Parser().parse(word)
    assert parts == Parser().parse(word).flat()
    assert RULE_NAME not in parsed.rules.flat()

    word = r"שָׁדַדְתְּ"  # sha-da-det (same place of articulation)
    parts = [
        "shin",
        "qamats-gadol",
        "dalet",
        "patah",
        "dalet",
        "sheva-nah",
        "tav",
        "dagesh-qal",
        "sheva-nah",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"שָׁלַלְתְּ"  # sha-lalt (negative example)
    parts = [
        "shin",
        "qamats-gadol",
        "lamed",
        "patah",
        "lamed",
        "sheva-nah",
        "tav",
        "dagesh-qal",
        "sheva-nah",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME not in parsed.rules.flat()


def test_modern_sheva_2():
    """`sheva` is voiced when under the first letter of a word, if this letter
    is a sonorant in modern pronunciation (`yod`, `lamed`, `mem`, `nun`, `resh`).
    """
    RULE_NAME = "sheva-modern-voiced-sonorant"

    word = r"נְמָלִים"  # ne-ma-lim
    parts = [
        "nun",
        "sheva-na",
        "mem",
        "qamats-gadol",
        "lamed",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"גְּמָלִים"  # ge-ma-lim (traditional); gma-lim (modern); (negative example)
    parts = [
        "gimel",
        "dagesh-qal",
        "sheva-na",
        "mem",
        "qamats-gadol",
        "lamed",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME not in parsed.rules.flat()

    word = r"מְנִיָּה"  # me-ni-ya
    parts = [
        "mem",
        "sheva-na",
        "nun",
        "hiriq",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
        "eim-qria-he",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"בְּנִיָּה"  # be-ni-ya (traditional); bni-ya (modern); (negative example)
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "nun",
        "hiriq",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
        "eim-qria-he",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME not in parsed.rules.flat()


def test_modern_sheva_3():
    """`sheva` is voiced when under the first letter of a word, if the second
    letter is a glottal consonant (`alef`, `he`, `ayin`).
    """
    RULE_NAME = "sheva-modern-voiced-before-glottal"

    word = r"תְּאָרִים"  # te-a-rim
    parts = [
        "tav",
        "dagesh-qal",
        "sheva-na",
        "alef",
        "qamats-gadol",
        "resh",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"תְּמָרִים"  # te-ma-rim (traditional); tma-rim (modern); (negative example)
    parts = [
        "tav",
        "dagesh-qal",
        "sheva-na",
        "mem",
        "qamats-gadol",
        "resh",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME not in parsed.rules.flat()


def test_modern_sheva_4():
    """`sheva` is voiced when under the first letter of a word, if this letter
    represents one of the prefix-morphemes (`be-`, `ve-`, `ke-`, `le-`, `te-`).
    """
    # TODO: requires root word to determine if the first letter is a prefix or not.
    RULE_NAME = "sheva-modern-voiced-prefix"

    word = r"בְּרֵיחָהּ"  # be-rei-cha
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "resh",
        "tsere",
        "eim-qria-yod",
        "het",
        "qamats-gadol",
        "mapiq-he",
        "mapiq",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"בְּרֵיכָה"  # brei-cha
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "resh",
        "tsere",
        "eim-qria-yod",
        "khaf",
        "qamats-gadol",
        "eim-qria-he",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    # assert RULE_NAME not in parsed.rules.flat()  # TODO: need base word

    # NOTE: requires emphasis information
    word = r"בְּחִישָׁה"  # be-chi-sha
    word = r"בְּחִישָׁה"  # bchi-sha

    # NOTE: requires emphasis information
    word = r"וְרוֹדִים"  # ve-ro-dim
    word = r"וְרוּדִים"  # vru-dim

    # NOTE: requires emphasis information
    word = r"כְּרָזָה"  # ke-ra-za
    word = r"כְּרָזָה"  # kra-za

    word = r"לְפָּרִיז"  # le-pa-rav
    parts = [
        "lamed",
        "sheva-na",
        "pe",
        "dagesh-qal",
        "qamats-gadol",
        "resh",
        "hiriq-male-yod",
        "eim-qria-yod",
        "zayin",
    ]
    parsed = Parser(disabled=["sheva-modern-voiced-sonorant"]).parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"תְּבַלּוּ"  # te-va-lu
    parts = [
        "tav",
        "dagesh-qal",
        "sheva-na",
        "vet",
        "patah",
        "lamed",
        "dagesh-hazaq",
        "shuruq",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    assert RULE_NAME in parsed.rules.flat()

    word = r"תְּבַלּוּל"
    parts = [
        "tav",
        "dagesh-qal",
        "sheva-na",
        "vet",
        "patah",
        "lamed",
        "dagesh-hazaq",
        "shuruq",
        "lamed",
    ]
    parsed = Parser().parse(word)
    assert parts == parsed.flat()
    # assert RULE_NAME not in parsed.rules.flat()  # TODO: need base word
