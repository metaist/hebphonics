#!/usr/bin/python
"""vowel, `glide-`"""

# pkg
from hebphonics.grammar import Parser

# vowel


def test_holam_haser_default():
    """default `holam` is `holam-haser` (vowel-holam-haser-default)"""
    word = r"צֹר"  # tsor (Exodus 4:25)
    parts = ["tsadi", "holam-haser", "resh"]
    assert parts == Parser().parse(word).flat()


def test_patah_genuvah():
    """`patah` on last `het|ayin|mapiq-he` is `patah-genuvah`"""
    # het
    word = r"נֹחַ"  # no-akh (Genesis 5:29)
    parts = ["nun", "holam-haser", "het", "patah-genuvah"]
    assert parts == Parser().parse(word).flat()

    # ayin
    word = r"רֹעַ"  # ro-a (Deuteronomy 28:20)
    parts = ["resh", "holam-haser", "ayin", "patah-genuvah"]
    assert parts == Parser().parse(word).flat()

    # mapiq-he
    word = r"נֹהַּ"  # no-ah (Ezekiel 7:11)
    parts = ["nun", "holam-haser", "mapiq-he", "mapiq", "patah-genuvah"]
    assert parts == Parser().parse(word).flat()


def test_glide_av():
    """bare `yod` after `qamats` before `vav` is `yod-glide` (glide-av)"""
    word = r"אֵלָיו"  # ei-lav (Leviticus 1:1)
    parts = ["alef", "tsere", "lamed", "qamats-gadol", "yod-glide", "vav"]
    assert parts == Parser().parse(word).flat()


def test_glide_ay_qamats():
    """bare `yod` after `qamats` is `yod-glide` (glide-ai-qamats)"""
    word = r"חָי"  # khai (Genesis 3:20)
    parts = ["het", "qamats-gadol", "yod-glide"]
    assert parts == Parser().parse(word).flat()


def test_glide_ay_patah():
    """bare `yod` after `patah` is `yod-glide` (glide-ai-patah)"""
    word = r"חַי"  # khai (Leviticus 13:10)
    parts = ["het", "patah", "yod-glide"]
    assert parts == Parser().parse(word).flat()


def test_glide_aiy():
    """`yod+hiriq` after `patah` is `yod-glide` (glide-aiy)"""
    word = r"מַיִם"  # ma-yim (Leviticus 11:34)
    parts = ["mem", "patah", "yod-glide", "hiriq", "mem-sofit"]
    assert parts == Parser().parse(word).flat()


def test_glide_oy():
    """bare `yod` after `holam` is `yod-glide` (glide-oy)"""
    word = r"אוֹי"  # oy (Numbers 21:29)
    parts = ["alef", "holam-male-vav", "yod-glide"]
    assert parts == Parser().parse(word).flat()


def test_glide_uy():
    """bare `yod` after `shuruq` is `yod-glide` (glide-uy)"""
    word = r"צִפּוּי"  # tsi-puy (Numbers 17:3)
    parts = ["tsadi", "hiriq", "pe", "dagesh-hazaq", "shuruq", "yod-glide"]
    assert parts == Parser().parse(word).flat()

    # words that start with shuruq don't count
    word = r"וּמִי"  # u-mi (Deuteronomy 4:8)
    parts = ["shuruq", "mem", "hiriq-male-yod", "eim-qria-yod"]
    assert parts == Parser().parse(word).flat()
