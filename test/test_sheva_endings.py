#!/usr/bin/python
"""`sheva-` endings

NOTE: These are empirically derrived rules, so they are subject to change.
"""

# pkg
from hebphonics.grammar import Parser

## `sheva-na`


def test_sheva_na_ending_sah():
    """`sheva` before `sav+qamats`, `he` is `sheva-na` (sheva-na-ending-sah)"""
    word = r"פָשְׂתָה"  # fa-se-sah (Leviticus 13:28)
    parts = [
        "fe",
        "qamats-gadol",
        "sin",
        "sheva-na",
        "sav",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()

    # non-doubled sound
    word = r"שָׁבְתָה"  # sha-ve-sa (Leviticus 26:35)
    parts = [
        "shin",
        "qamats-gadol",
        "vet",
        "sheva-na",
        "sav",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_ending_alkhf_ah():
    """`sheva` after `gimel|yod|mem` before `alef|khaf|lamed|fe + qamats`, `he` is `sheva-na` (sheva-na-ending-a|kh|l|f-ah)"""
    # gimel, lamed
    word = r"גָדְלָה"  # ga-de-lah (Genesis 19:13)
    parts = [
        "gimel",
        "qamats-gadol",
        "dalet",
        "sheva-na",
        "lamed",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()

    # yod, lamed
    word = r"יָכְלָה"  # ya-khe-lah (Exodus 2:3)
    parts = [
        "yod",
        "qamats-gadol",
        "khaf",
        "sheva-na",
        "lamed",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()

    # yod, fe
    word = r"יָסְפָה"  # ya-se-fah (Genesis 8:12)
    parts = [
        "yod",
        "qamats-gadol",
        "samekh",
        "sheva-na",
        "fe",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()

    # mem, alef
    word = r"מָלְאָה"  # ma-le-ah (Genesis 6:13)
    parts = [
        "mem",
        "qamats-gadol",
        "lamed",
        "sheva-na",
        "alef",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()

    # mem, khaf
    word = r"מָשְׁכָה"  # ma-she-kha (Deuteronomy 21:3)
    parts = [
        "mem",
        "qamats-gadol",
        "shin",
        "sheva-na",
        "khaf",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_shuruq_end():
    """`sheva` before `shuruq` at end of word is `sheva-na` (sheva-na-ending-shuruq)"""
    word = r"יָרְאוּ"  # ya-re-u (Exodus 1:21)
    parts = ["yod", "qamats-gadol", "resh", "sheva-na", "alef", "shuruq"]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_khaf_sofit_qamats():
    """`sheva` on `lamed|shin|sav` before `khaf-sofit+qamats-gadol` is `sheva-na` (sheva-na-ending-l|sh|s-kha)"""
    # lamed
    word = r"יִשְׁאָלְךָ"  # yish-ale-kha (Deuteronomy 6:20)
    parts = [
        "yod",
        "hiriq",
        "shin",
        "sheva-nah",
        "alef",
        "qamats-gadol",
        "lamed",
        "sheva-na",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()

    # shin
    word = r"יִירָשְׁךָ"  # yi-ra-she-kha (Genesis 15:4)
    parts = [
        "yod",
        "hiriq-male-yod",
        "eim-qria-yod",
        "resh",
        "qamats-gadol",
        "shin",
        "sheva-na",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()

    # sav
    word = r"בְּכֹרָתְךָ"  # be-kho-ra-te-kha (Genesis 25:31)
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "khaf",
        "holam-haser",
        "resh",
        "qamats-gadol",
        "sav",
        "sheva-na",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_na_tsere_mem_sofit():
    """`sheva` after non-guttural before `tsere`, `mem-sofit` is `sheva-na` (sheva-na-ending-tsere-mem-sofit)"""
    word = r"וַיְבָרְכֵם"  # vay-va-re-kheim (Leviticus 9:22)
    parts = [
        "vav",
        "patah",
        "yod",
        "sheva-merahef",
        "vet",
        "qamats-gadol",
        "resh",
        "sheva-na",
        "khaf",
        "tsere",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()


## `sheva-nah`

### `he`


def test_sheva_nah_ending_iah():
    """`sheva` before `hiriq`, `qamats`, `he` is `sheva-nah` (sheva-nah-ending-iah)"""
    word = r"נָכְרִיָּה"  # nokh-ri-yah (Exodus 2:22)
    parts = [
        "nun",
        "qamats-qatan",
        "khaf",
        "sheva-nah",
        "resh",
        "hiriq",
        "yod",
        "dagesh-hazaq",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_ah():
    """`sheva` before `qamats`, `he` is `sheva-nah` (sheva-nah-ending-ah)"""
    word = r"וְהָרְאָה"  # ve-hor-ah (Leviticus 13:49)
    parts = [
        "vav",
        "sheva-na",
        "he",
        "qamats-qatan",
        "resh",
        "sheva-nah",
        "alef",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()


### `vav`


def test_sheva_nah_ending_o():
    """`sheva` before `holam-male` is `sheva-nah` (sheva-nah-ending-o)"""
    word = r"אָזְנוֹ"  # oz-no (Exodus 21:6)
    parts = ["alef", "qamats-qatan", "zayin", "sheva-nah", "nun", "holam-male-vav"]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_av():
    """`sheva` before `qamats`, `yod`, `vav` is `sheva-nah` (sheva-nah-ending-av)"""
    word = r"חָפְנָיו"  # khof-nav (Leviticus 16:12)
    parts = [
        "het",
        "qamats-qatan",
        "fe",
        "sheva-nah",
        "nun",
        "qamats-gadol",
        "yod-glide",
        "vav",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_vowel_letter_vav_vowel():
    """`sheva` before `qamats|tsere`, `nun|sav`, `shuruq|holam-male` is `sheva-nah` (sheva-nah-ending-shuruq|holam-male)"""
    # qamats-sav-shuruq
    # no example

    # qamats-sav-holam-male
    word = r"עָרְלָתוֹ"  # or-la-to (Leviticus 12:3)
    parts = [
        "ayin",
        "qamats-qatan",
        "resh",
        "sheva-nah",
        "lamed",
        "qamats-gadol",
        "sav",
        "holam-male-vav",
    ]
    assert parts == Parser().parse(word).flat()

    # qamats-nun-shuruq
    word = r"וְשָׂכְלְתָנוּ"
    parts = [
        "vav",
        "sheva-na",
        "sin",
        "qamats-qatan",
        "khaf",
        "sheva-nah",
        "lamed",
        "sheva-na",
        "sav",
        "qamats-gadol",
        "nun",
        "shuruq",
    ]
    assert parts == Parser().parse(word).flat()

    # qamats-nun-holam-male
    word = r"קָרְבָּנוֹ"
    parts = [
        "qof",
        "qamats-qatan",
        "resh",
        "sheva-nah",
        "bet",
        "dagesh-qal",
        "qamats-gadol",
        "nun",
        "holam-male-vav",
    ]
    assert parts == Parser().parse(word).flat()

    # tsere-sav-shuruq
    # no example

    # tsere-sav-holam-male
    # no example

    # tsere-nun-shuruq
    word = r"עָנְיֵנוּ"  # on-yei-nu (Deutoronomy 26:7)
    parts = [
        "ayin",
        "qamats-qatan",
        "nun",
        "sheva-nah",
        "yod",
        "tsere",
        "nun",
        "shuruq",
    ]
    assert parts == Parser().parse(word).flat()

    # tsere-nun-holam-male
    # no example


### `yod`


def test_sheva_nah_vowel_yod_end():
    """`sheva` before `hiriq|tsere|patah|qamats`, `yod` is `sheva-nah` (sheva-nah-ending-vowel-yod)"""
    # hiriq
    word = r"וְהָעָפְנִי"  # ve-ha-of-ni (Joshua 18:24)
    parts = [
        "vav",
        "sheva-na",
        "he",
        "qamats-gadol",
        "ayin",
        "qamats-qatan",
        "fe",
        "sheva-nah",
        "nun",
        "hiriq-male-yod",
        "eim-qria-yod",
    ]
    assert parts == Parser().parse(word).flat()

    # hiriq-male
    word = r"עָנְיִי"  # on-yi (Genesis 31:42)
    parts = [
        "ayin",
        "qamats-qatan",
        "nun",
        "sheva-nah",
        "yod",
        "hiriq-male-yod",
        "eim-qria-yod",
    ]
    assert parts == Parser().parse(word).flat()

    # tsere
    word = r"קָדְשֵׁי"  # kod-shei (Leviticus 22:15)
    parts = [
        "qof",
        "qamats-qatan",
        "dalet",
        "sheva-nah",
        "shin",
        "tsere",
        "eim-qria-yod",
    ]
    assert parts == Parser().parse(word).flat()

    # patah
    word = r"בְּאָזְנַי"  # be-oz-nai
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "alef",
        "qamats-qatan",
        "zayin",
        "sheva-nah",
        "nun",
        "patah",
        "yod-glide",
    ]
    assert parts == Parser().parse(word).flat()

    # qamats
    word = r"בְּאָזְנָי"  # be-oz-nai
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "alef",
        "qamats-qatan",
        "zayin",
        "sheva-nah",
        "nun",
        "qamats-gadol",
        "yod-glide",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_tsere_hiriq_male():
    """`sheva` before `tsere`, `hiriq-male` is `sheva-nah` (sheva-nah-ending-tsere-hiriq-male)"""
    word = r"הָרְגֵנִי"  # hor-gei-ni (Numbers 11:15)
    parts = [
        "he",
        "qamats-qatan",
        "resh",
        "sheva-nah",
        "gimel",
        "tsere",
        "nun",
        "hiriq-male-yod",
        "eim-qria-yod",
    ]
    assert parts == Parser().parse(word).flat()


### `khaf-sofit`


def test_sheva_nah_ending_eikh():
    """`sheva` before `tsere`, `khaf-sofit` is `sheva-nah` (sheva-nah-ending-eikh)"""
    word = r"עָנְיֵךְ"  # on-yeikh (Genesis 16:11)
    parts = [
        "ayin",
        "qamats-qatan",
        "nun",
        "sheva-nah",
        "yod",
        "tsere",
        "khaf-sofit",
        "sheva-nah",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_khaf_sofit_after_segol():
    """`sheva` before `segol`, `khaf-sofit+qamats` is `sheva-nah` (sheva-nah-ending-khaf-sofit-after-segol)"""
    word = r"אָכְלֶךָ"  # okh-le-kha
    parts = [
        "alef",
        "qamats-qatan",
        "khaf",
        "sheva-nah",
        "lamed",
        "segol",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_khaf_sofit_after_segol_yod():
    """`sheva` before `segol`, `yod`, `khaf-sofit+qamats` is `sheva-nah` (sheva-nah-ending-khaf-sofit-after-segol-yod)"""
    word = r"בְּאָזְנֶיךָ"  # be-oz-ne-kha
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "alef",
        "qamats-qatan",
        "zayin",
        "sheva-nah",
        "nun",
        "segol",
        "eim-qria-yod",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_khaf_sofit_after_qamats_segol():
    """`sheva` before `qamats`, `segol`, `khaf-sofit+qamats` is `sheva-nah` (sheva-nah-ending-khaf-sofit-after-qamats-segol)"""
    word = r"חָכְמָתֶךָ"  # khokh-ma-te-kha
    parts = [
        "het",
        "qamats-qatan",
        "khaf",
        "sheva-nah",
        "mem",
        "qamats-gadol",
        "sav",
        "segol",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_khaf_sofit_after_hataf():
    """`sheva` after `hataf-`, `qamats` and before `khaf-sofit+qamats` is `sheva-nah` (sheva-nah-ending-khaf-sofit-after-hataf)"""
    word = r"אֲכָלְךָ"  # o-khol-kha
    parts = [
        "alef",
        "hataf-patah",
        "khaf",
        "qamats-qatan",
        "lamed",
        "sheva-nah",
        "khaf-sofit",
        "qamats-gadol",
    ]
    assert parts == Parser().parse(word).flat()


### `mapiq-he`, `mem-sofit`, `nun-sofit`


def test_sheva_nah_qamats_letter_end():
    """`sheva` before `qamats`, (`mapiq-he|mem-sofit|nun-sofit`) is `sheva-nah` (sheva-nah-ending-qamats-letter)"""
    # qamats-mapiq-he
    word = r"לְעָבְדָהּ"  # le-ov-dah (Genesis 2:15)
    parts = [
        "lamed",
        "sheva-na",
        "ayin",
        "qamats-qatan",
        "vet",
        "sheva-nah",
        "dalet",
        "qamats-gadol",
        "mapiq-he",
        "mapiq",
    ]
    assert parts == Parser().parse(word).flat()

    # qamats-mem-sofit
    word = r"אָכְלָם"  # okh-lam (Genesis 14:11)
    parts = [
        "alef",
        "qamats-qatan",
        "khaf",
        "sheva-nah",
        "lamed",
        "qamats-gadol",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    # qamats-nun-sofit
    word = r"יָקְטָן"  # yok-tan (Genesis 10:25)
    parts = [
        "yod",
        "qamats-qatan",
        "qof",
        "sheva-nah",
        "tet",
        "qamats-gadol",
        "nun-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    # segol-mapiq-he
    # no example

    # segol-mem-sofit
    word = r"חָקְכֶם"
    parts = ["het", "qamats-qatan", "qof", "sheva-nah", "khaf", "segol", "mem-sofit"]
    assert parts == Parser().parse(word).flat()

    # segol-nun-sofit
    # no example


### `mem-sofit`


def test_sheva_nah_guttural_tsere_mem_sofit():
    """`sheva` after guttural before `tsere`, `mem-sofit` is `sheva-na` (sheva-nah-ending-guttural-tsere-mem-sofit)"""
    word = r"תָעָבְדֵם"  # ta-ov-deim (Deutoronomy 5:8)
    parts = [
        "sav",
        "qamats-gadol",
        "ayin",
        "qamats-qatan",
        "vet",
        "sheva-nah",
        "dalet",
        "tsere",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_qamats_qamats_mem_sofit():
    """`sheva` before `qamats`, `qamats`, `he|mem-sofit|nun-sofit` is `sheva-nah` (sheva-nah-ending-a-a-h|m|n)"""
    # he
    word = r"בְּיָטְבָתָה"  # be-yot-va-sa (Numbers 33:33)
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "yod",
        "qamats-qatan",
        "tet",
        "sheva-nah",
        "vet",
        "qamats-gadol",
        "sav",
        "qamats-gadol",
        "eim-qria-he",
    ]
    assert parts == Parser().parse(word).flat()

    # mapiq-he
    word = r"בְּחָכְמָתָהּ"  # be-khokh-ma-tah (II Samuel 20:22)
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "het",
        "qamats-qatan",
        "khaf",
        "sheva-nah",
        "mem",
        "qamats-gadol",
        "sav",
        "qamats-gadol",
        "mapiq-he",
        "mapiq",
    ]
    assert parts == Parser().parse(word).flat()

    # mem-sofit
    word = r"מָשְׁחָתָם"  # mosh-kha-tam
    parts = [
        "mem",
        "qamats-qatan",
        "shin",
        "sheva-nah",
        "het",
        "qamats-gadol",
        "sav",
        "qamats-gadol",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    # nun-sofit
    word = "כָרְסָוָן"  # qor-sa-van (Daniel 7:9) # TODO: verify
    parts = [
        "khaf",
        "qamats-qatan",
        "resh",
        "sheva-nah",
        "samekh",
        "qamats-gadol",
        "vav",
        "qamats-gadol",
        "nun-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_tsere_segol_mem_sofit():
    """`sheva` before `tsere`, `yod`, `segol`, `mem-sofit` is `sheva-nah` (sheva-nah-ending-tsere-yod-segol-mem-sofit)"""
    word = r"בְּאָזְנֵיכֶם"  # be-oz-nei-khem
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "alef",
        "qamats-qatan",
        "zayin",
        "sheva-nah",
        "nun",
        "tsere",
        "eim-qria-yod",
        "khaf",
        "segol",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_ai_m_kh():
    """`sheva` before `qamats|patah`, `hiriq`, `khaf-sofit|mem-sofit` is `sheva-nah` (sheva-nah-ending-ai-m|kh)"""
    word = r"הָאָבְנָיִם"  # ha-ov-na-im (Exodus 1:15)
    parts = [
        "he",
        "qamats-gadol",
        "alef",
        "qamats-qatan",
        "vet",
        "sheva-nah",
        "nun",
        "qamats-gadol",
        "yod",
        "hiriq",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()


### `tav` / `sav`


def test_sheva_nah_ending_os():
    """`sheva` before letter, `holam-male`, `sav` is `sheva-nah` (sheva-nah-ending-os)"""
    word = r"כָּתְנוֹת"  # kot-not
    parts = [
        "kaf",
        "dagesh-qal",
        "qamats-qatan",
        "sav",
        "sheva-nah",
        "nun",
        "holam-male-vav",
        "sav",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_iym_iys():
    """`sheva` before `hiriq`, `yod`, `mem-sofit|sav` is `sheva-nah` (sheva-nah-ending-iy-m|s)"""
    # mem-sofit
    word = "בָּטְנִים"  # bot-nim (Genesis 43:11)
    parts = [
        "bet",
        "dagesh-qal",
        "qamats-qatan",
        "tet",
        "sheva-nah",
        "nun",
        "hiriq-male-yod",
        "eim-qria-yod",
        "mem-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    # sav
    word = r"גָּפְרִית"  # gof-ris (Deuteronomy 29:22)
    parts = [
        "gimel",
        "dagesh-qal",
        "qamats-qatan",
        "fe",
        "sheva-nah",
        "resh",
        "hiriq-male-yod",
        "eim-qria-yod",
        "sav",
    ]
    assert parts == Parser().parse(word).flat()


def test_sheva_nah_ending_a_dnrs():
    """`sheva` before `patah`, `dalet|nun-sofit|ayin|sav` is `sheva-nah` (sheva-nah-ending-a-d|n|r|s)"""
    # patah, dalet
    word = r"הָפְקַד"  # hof-kad (Leviticus 5:23)
    parts = ["he", "qamats-qatan", "fe", "sheva-nah", "qof", "patah", "dalet"]
    assert parts == Parser().parse(word).flat()

    # qamats, dalet
    word = r"צְלָפְחָד"  # tse-lof-khad (Numbers 26:33)
    parts = [
        "tsadi",
        "sheva-na",
        "lamed",
        "qamats-qatan",
        "fe",
        "sheva-nah",
        "het",
        "qamats-gadol",
        "dalet",
    ]
    assert parts == Parser().parse(word).flat()

    # patah, nun-sofit
    word = r"בְּאָבְדַן"  # be-ov-dan (Esther 8:6)
    parts = [
        "bet",
        "dagesh-qal",
        "sheva-na",
        "alef",
        "qamats-qatan",
        "vet",
        "sheva-nah",
        "dalet",
        "patah",
        "nun-sofit",
    ]
    assert parts == Parser().parse(word).flat()

    # qamats, nun-sofit
    # no example

    # patah, ayin
    word = r"חָפְרַע"  # khof-ra (Jeremiah 44:30)
    parts = ["het", "qamats-qatan", "fe", "sheva-nah", "resh", "patah", "ayin"]
    assert parts == Parser().parse(word).flat()

    # qamats, ayin
    # no example

    # patah, resh
    # no example

    # qamats, resh
    word = r"מָשְׁזָר"  # mosh-zar (Exodus 26:1)
    parts = [
        "mem",
        "qamats-qatan",
        "shin",
        "sheva-nah",
        "zayin",
        "qamats-gadol",
        "resh",
    ]
    assert parts == Parser().parse(word).flat()

    # patah, sav
    word = r"חָכְמַת"  # khokh-mas (Exodus 35:35)
    parts = ["het", "qamats-qatan", "khaf", "sheva-nah", "mem", "patah", "sav"]
    assert parts == Parser().parse(word).flat()

    # qamats, sav
    word = r"גָּלְיָת"  # gol-yat (I Samuel 17:4)
    parts = [
        "gimel",
        "dagesh-qal",
        "qamats-qatan",
        "lamed",
        "sheva-nah",
        "yod",
        "qamats-gadol",
        "sav",
    ]
    assert parts == Parser().parse(word).flat()
