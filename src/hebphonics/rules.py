#!/usr/bin/env python
# coding: utf-8
"""Rules of Hebrew grammar.

For an overview and references, see [hebrew-grammar.md][1].

[1]:
"""
PARSE_CODES = {
    # syllables
    "H001": ("syl-before-vowel", "syllable break before a vowel"),
    "H002": ("syl-around-sheva-na", "syllable break before and after `sheva-na`"),
    "H003": ("syl-none-after-hataf", "(strict) no syllable break after hataf-vowel"),
    # `dagesh-`
    "H101": ("dagesh-mapiq-alef", "`dagesh` in `alef` is `mapiq-alef`"),
    "H102": ("dagesh-mapiq-he", "`dagesh` in last `he` is `mapiq-he`"),
    "H103": ("dagesh-hazaq-he", "`dagesh` in non-last `he` is `dagesh-hazaq`"),
    "H104": ("dagesh-hazaq-bgdkft", "`dagesh` in BGDKFT after vowel is `dagesh-hazaq`"),
    "H105": ("dagesh-qal-bgdkft", "`dagesh` in BGDKFT NOT after vowel is `dagesh-qal`"),
    "H106": ("dagesh-hazaq-other", "any other `dagesh` is a `dagesh-hazaq`"),
    # `sheva-`
    "H201": ("sheva-na-word-start", "`sheva` at word start is `sheva-na`"),
    "H202": ("sheva-nah-word-end", "`sheva` at the end of a word is `sheva-nah`"),
    "H203": ("sheva-na-dagesh-hazaq", "`sheva` under `dagesh-hazaq` is `sheva-na`"),
    "H204": ("sheva-na-after-long-vowel", "`sheva` after long vowel is `sheva-na`"),
    "H205": ("sheva-nah-after-short-vowel", "`sheva` after short vowel is `sheva-nah`"),
    "H206": ("sheva-nah-alef-end", "`sheva` before last bare `alef` is `sheva-nah`"),
    "H207": ("sheva-na-double-letter", "`sheva` before same letter is `sheva-na`"),
    "H208": ("sheva-double-midword", "two `sheva` midword are `sheva-nah`, `sheva-na`"),
    "H209": ("sheva-double-end", "two `sheva` at word end are `sheva-na`, `sheva-na`"),
    # `-male`
    "H301": ("male-hiriq", "`hiriq` before bare `yod` is `hiriq-male`"),
    "H302": ("male-tsere", "`tsere` before bare `alef|he|yod` is `tsere-male`"),
    "H303": ("male-segol", "`segol` before bare `alef|he|yod` is `segol-male`"),
    "H304": ("male-patah", "`patah` before bare `alef|he` is `patah-male`"),
    "H305": ("male-qamats", "`qamats` before bare `alef|he` is `qamats-male`"),
    "H306": ("male-holam", "`holam` before bare `alef|he` is `holam-male`"),
    # `patah-genuvah`
    "H401": ("patah-genuvah", "`patah` on last `het|ayin|mapiq-he` is `patah-genuvah`"),
    # `qamats-qatan`
    "H501": (  # TODO
        "qq-unstressed-closed",
        "`qamats` in unstressed closed syllable is `qamats-qatan`",
    ),
    "H502": ("qq-maqaf", "`qamats` in non-last word with `maqaf` is `qamats-qatan`"),
    "H503": ("qq-hataf-qamats", "`qamats` before `hataf-qamats` is `qamats-qatan`"),
    "H504": (  # TODO
        "qq-be-le-prefix",
        "`qamats` in unstressed syllable after `be|le`-prefix is `qamtas-qatan`",
    ),
    # `vav`
    "H601": (
        "vav-holam-haser-unicode",
        "`VAV` followed by `HOLAM_HASER_FOR_VAV` is `vav`, `holam-haser`",
    ),
    "H602": (
        "vav-is-holam-male",
        "`vav`, `HOLAM_HASER` NOT after vowel or sheva is `holam-male`",
    ),
    "H603": (
        "vav-holam-haser",
        "`VAV` with `HOLAM_HASER` after vowel or sheva `vav`, `holam-haser`",
    ),
    "H604": ("vav-is-shurug", "`VAV` with `DAGESH` NOT after vowel is `shuruq`"),
    "H605": (
        "vav-dagesh-hazaq",
        "`VAV` with `DAGESH` after/has vowel is `vav`, `dagesh-hazaq`",
    ),
}
"""Descriptions of the HebPhonics parse rules."""

PARSE_NAMES = {}
for code, (name, desc) in PARSE_CODES.items():
    PARSE_NAMES[name] = (code, desc)
    val = f"{code}: {desc} ({name})"
    locals().update({code: val, name.upper().replace("-", "_"): val})
