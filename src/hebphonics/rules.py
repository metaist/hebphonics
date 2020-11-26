#!/usr/bin/env python
# coding: utf-8
"""Rules of Hebrew grammar.

For an overview and references, see [hebrew-grammar.md][1].

[1]: https://github.com/metaist/hebphonics/blob/master/doc/hebrew-grammar.md
"""

# native
from typing import Callable

# pkg
from . import tokens as T

BEGEDKEFET = {
    # {<unicode name>: (<name WITHOUT dagesh>, <name WITH dagesh>)
    T.LETTER_BET: (T.NAME_VET, T.NAME_BET),
    T.LETTER_GIMEL: (T.NAME_GIMEL, T.NAME_GIMEL),
    T.LETTER_DALET: (T.NAME_DALET, T.NAME_DALET),
    T.LETTER_KAF: (T.NAME_KHAF, T.NAME_KAF),
    T.LETTER_FINAL_KAF: (T.NAME_KHAF_SOFIT, T.NAME_KAF_SOFIT),
    T.LETTER_PE: (T.NAME_FE, T.NAME_PE),
    T.LETTER_FINAL_PE: (T.NAME_FE_SOFIT, T.NAME_PE_SOFIT),
    T.LETTER_TAV: (T.NAME_SAV, T.NAME_TAV),
}
"""BeGeDKeFeT letters have altered names when followed by a dagesh."""

ALEF_HE = [T.NAME_ALEF, T.NAME_HE]
ALEF_HE_YOD = [T.NAME_ALEF, T.NAME_HE, T.NAME_YOD]

NIQQUD_DAGESH = "dagesh"
NIQQUD_SHEVA = "sheva"
NIQQUD_HATAF = "hataf"
NIQQUD_LONG = "long"
NIQQUD_SHORT = "short"
NIQQUD_TYPES = {
    T.NAME_MAPIQ: NIQQUD_DAGESH,
    T.NAME_DAGESH: NIQQUD_DAGESH,
    T.NAME_DAGESH_QAL: NIQQUD_DAGESH,
    T.NAME_DAGESH_HAZAQ: NIQQUD_DAGESH,
    #
    T.NAME_SHEVA: NIQQUD_SHEVA,
    T.NAME_SHEVA_NA: NIQQUD_SHEVA,
    T.NAME_SHEVA_NAH: NIQQUD_SHEVA,
    #
    T.NAME_HATAF_SEGOL: NIQQUD_HATAF,
    T.NAME_HATAF_PATAH: NIQQUD_HATAF,
    T.NAME_HATAF_QAMATS: NIQQUD_HATAF,
    #
    T.NAME_HIRIQ: NIQQUD_SHORT,
    T.NAME_HIRIQ_MALE_YOD: NIQQUD_LONG,
    #
    T.NAME_TSERE: NIQQUD_LONG,
    T.NAME_TSERE_MALE_ALEF: NIQQUD_LONG,
    T.NAME_TSERE_MALE_HE: NIQQUD_LONG,
    T.NAME_TSERE_MALE_YOD: NIQQUD_LONG,
    #
    T.NAME_SEGOL: NIQQUD_SHORT,
    T.NAME_SEGOL_MALE_ALEF: NIQQUD_SHORT,
    T.NAME_SEGOL_MALE_HE: NIQQUD_SHORT,
    T.NAME_SEGOL_MALE_YOD: NIQQUD_SHORT,
    #
    T.NAME_PATAH: NIQQUD_SHORT,
    T.NAME_PATAH_MALE_ALEF: NIQQUD_SHORT,
    T.NAME_PATAH_MALE_HE: NIQQUD_SHORT,
    T.NAME_PATAH_GENUVAH: NIQQUD_SHORT,
    #
    T.NAME_QAMATS: NIQQUD_LONG,
    T.NAME_QAMATS_GADOL: NIQQUD_LONG,
    T.NAME_QAMATS_MALE_ALEF: NIQQUD_LONG,
    T.NAME_QAMATS_MALE_HE: NIQQUD_LONG,
    T.NAME_QAMATS_QATAN: NIQQUD_SHORT,
    #
    T.NAME_HOLAM_HASER: NIQQUD_LONG,
    T.NAME_HOLAM_MALE_ALEF: NIQQUD_LONG,
    T.NAME_HOLAM_MALE_HE: NIQQUD_LONG,
    T.NAME_HOLAM_MALE_VAV: NIQQUD_LONG,
    #
    T.NAME_QUBUTS: NIQQUD_SHORT,
    T.NAME_SHURUQ: NIQQUD_LONG,
}
"""Categories of niqqud."""


def isvowel(point: str) -> str:
    """Return True if the point name is a vowel.

    >>> isvowel(T.NAME_QAMATS)
    True
    """
    return niqqudtype(point) in [NIQQUD_HATAF, NIQQUD_SHORT, NIQQUD_LONG]


def niqqudtype(point: str) -> str:
    """Return the type of point or None.

    Args:
        point (str): the grammatical name of the point

    Returns:
        str or None. The type of point ('hataf', 'short', 'long', 'sheva', or
        'dagesh') or None if the name is not a name of a point.

    Examples:
    >>> niqqudtype('hataf-segol') == NIQQUD_HATAF
    True
    >>> niqqudtype('qubuts') == NIQQUD_SHORT
    True
    >>> niqqudtype('sheva-nah') == NIQQUD_SHEVA
    True
    >>> niqqudtype('dagesh-hazaq') == NIQQUD_DAGESH
    True
    >>> niqqudtype('alef') is None
    True
    >>> niqqudtype(None) is None
    True
    """
    return NIQQUD_TYPES.get(point)


RULES = {}

STAGES = {
    "vav": [],
    "dagesh": [],
    "male": [],
    "vowel": [],
    "sheva": [],
    "last": [],
}


def rule(stage, name) -> Callable:
    """Label a rule with a name."""

    def generator(original: Callable) -> Callable:
        original.rule = name
        STAGES[stage].append(original)
        RULES[name] = f"{original.__doc__} ({stage}:{name})"
        return original

    return generator


# pylint: disable=inconsistent-return-statements

## `vav`


@rule("vav", "shuruq-start")
def shuruq_start(isfirst, guess):
    """`vav` with `dagesh` at start of word of word is `shuruq`"""
    if isfirst and guess.has(letter=T.NAME_VAV, dagesh=True, vowel=False):
        return guess.reset().update(vowel=T.NAME_SHURUQ, isopen=True)


@rule("vav", "vav-is-shuruq")
def vav_is_shuruq(guess, next_guess):
    """`vav` with `dagesh` NOT after vowel is `shuruq`"""
    is_shuruq = next_guess.has(letter=T.NAME_VAV, dagesh=True, vowel=False)
    if not guess.vowel and is_shuruq:
        next_guess.reset()
        return guess.update(vowel=T.NAME_SHURUQ, isopen=True)


@rule("vav", "vav-is-holam-male")
def vav_is_holam_male(guess, next_guess):
    """`vav` with `holam` NOT after vowel is `holam-male-vav`"""
    is_holam = next_guess.has(letter=T.NAME_VAV, vowel=T.NAME_HOLAM, dagesh="")
    if not guess.vowel and is_holam:
        next_guess.reset()
        return guess.update(vowel=T.NAME_HOLAM_MALE_VAV, isopen=True)


## `dagesh-`, `mapiq-`


@rule("dagesh", "mapiq-alef")
def mapiq_alef(token, guess):
    """`dagesh` in `alef` is `mapiq-alef` (rare)"""
    if token.has(letter=T.LETTER_ALEF, dagesh=True):
        return guess.update(letter=T.NAME_MAPIQ_ALEF, dagesh=T.NAME_MAPIQ)


@rule("dagesh", "mapiq-he")
def mapiq_he(token, guess, islast):
    """`dagesh` in last `he` is `mapiq-he`"""
    if islast and token.has(letter=T.LETTER_HE, dagesh=True):
        return guess.update(letter=T.NAME_MAPIQ_HE, dagesh=T.NAME_MAPIQ)


@rule("dagesh", "he-dagesh-hazaq")
def he_dagesh_hazaq(token, guess, islast):
    """`dagesh` in non-last `he` is `dagesh-hazaq` (non-standard)"""
    if not islast and token.has(letter=T.LETTER_HE, dagesh=True):
        return guess.update(dagesh=T.NAME_DAGESH_HAZAQ)


@rule("dagesh", "bgdkft-without-dagesh")
def bgdkft_without_dagesh(token, guess):
    """BGDKFT letter without dagesh has a different name"""
    if token.has(letter=BEGEDKEFET, dagesh=False):
        guess.letter, _ = BEGEDKEFET[token.letter]
        return guess


@rule("dagesh", "bgdkft-dagesh-hazaq")
def bgdkft_dagesh_hazaq(token, prev, guess):
    """`dagesh` in BGDKFT after vowel is `dagesh-hazaq`"""
    if token.has(letter=BEGEDKEFET, dagesh=True) and isvowel(prev.vowel):
        _, guess.letter = BEGEDKEFET[token.letter]
        guess.dagesh = T.NAME_DAGESH_HAZAQ
        return guess


@rule("dagesh", "bgdkft-dagesh-qal")
def bgdkft_dagesh_qal(token, prev, guess):
    """`dagesh` in BGDKFT NOT after vowel is `dagesh-qal`"""
    if token.has(letter=BEGEDKEFET, dagesh=True) and not isvowel(prev.vowel):
        _, guess.letter = BEGEDKEFET[token.letter]
        guess.dagesh = T.NAME_DAGESH_QAL
        return guess


@rule("dagesh", "dagesh-hazaq-default")
def dagesh_hazaq_default(guess):
    """default dagesh is `dagesh-hazaq`"""
    if T.NAME_DAGESH == guess.dagesh:
        guess.dagesh = T.NAME_DAGESH_HAZAQ
        return guess


## `male-`


@rule("male", "hiriq-male")
def hiriq_male(guess, next_guess):
    """`hiriq` before bare `yod` is `hiriq-male`"""
    if guess.vowel == T.NAME_HIRIQ and next_guess.isbare(T.NAME_YOD):
        guess.vowel = T.NAME_HIRIQ_MALE_YOD
        next_guess.isopen = True
        return guess


@rule("male", "tsere-segol-male")
def tsere_segol_male(guess, next_guess):
    """`tsere|segol` before bare `alef|he|yod` is `-male`"""
    if guess.vowel in [T.NAME_TSERE, T.NAME_SEGOL] and next_guess.isbare(ALEF_HE_YOD):
        guess.vowel += f"-male-{next_guess.letter}"
        next_guess.isopen = True
        return guess


@rule("male", "patah-qamats-holam-male")
def patah_qamats_holam_male(guess, next_guess):
    """`patah|qamats|holam` before bare `alef|he` is `-male`"""
    check = [T.NAME_PATAH, T.NAME_QAMATS, T.NAME_HOLAM]
    if guess.vowel in check and next_guess.isbare(ALEF_HE):
        guess.vowel += f"-male-{next_guess.letter}"
        next_guess.isopen = True
        return guess


@rule("male", "holam-haser-default")
def holam_haser_default(guess):
    """default `holam` is `holam-haser`"""
    if guess.vowel == T.NAME_HOLAM:
        return guess.update(vowel=T.NAME_HOLAM_HASER, isopen=True)


## vowel


@rule("vowel", "patah-genuvah")
def patah_genuvah(guess, islast):
    """`patah` on last `het|ayin|mapiq-he` is `patah-genuvah`"""
    check = [T.NAME_HET, T.NAME_AYIN, T.NAME_MAPIQ_HE]
    if islast and guess.has(letter=check, vowel=T.NAME_PATAH):
        return guess.update(vowel=T.NAME_PATAH_GENUVAH, isopen=False)  # constant sound


@rule("vowel", "qamats-gadol-meteg")
def qamats_gadol_meteg(token, guess):
    """`qamats` with `meteg` is `qamats-gadol`"""
    if T.NAME_QAMATS == guess.vowel and T.POINT_METEG in token.points:
        guess.vowel = T.NAME_QAMATS_GADOL
        return guess


@rule("vowel", "qamats-gadol-accent")
def qamats_gadol_accent(token, guess):
    """`qamats` with accent is `qamats-gadol`"""
    if T.NAME_QAMATS == guess.vowel and token.accents:
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("vowel", "qamats-qatan-before-hataf-qamats")
def qamats_qatan_before_hataf_qamats(token, guess, next_guess):
    """`qamats` without meteg immediately before `hataf-qamats` is `qamats-qatan`"""
    if (
        T.NAME_QAMATS == guess.vowel
        and T.POINT_METEG not in token.points
        and T.NAME_HATAF_QAMATS == next_guess.vowel
    ):
        return guess.update(vowel=T.NAME_QAMATS_QATAN)


@rule("last", "qamats-qatan-before-midword-sheva-nah")
def qamats_qatan_before_sheva_nah(neg_idx, guess, next_guess):
    """`qamats` before midword `sheva-nah` is `qamats-qatan`"""
    if (
        neg_idx > 1
        and T.NAME_QAMATS == guess.vowel
        and T.NAME_SHEVA_NAH == next_guess.vowel
    ):
        return guess.update(vowel=T.NAME_QAMATS_QATAN)


@rule("last", "qamats-gadol-open-syllable")
def qamats_gadol_open_syllable(guess, next_guess):
    """`qamats` in open syllable is `qamats-gadol`"""
    if T.NAME_QAMATS == guess.vowel and next_guess.isopen:
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


# @rule("vowel", "qamats-qatan-in-maqaf")
# def qamats_qatan_in_maqaf(token, guess, next_guess, uni):
#     """`qamats` in closed syllable in non-last word with `maqaf` is `qamats-qatan`"""
#     if (
#         T.NAME_QAMATS == guess.vowel
#         and not next_guess.isopen
#         and T.POINT_METEG not in token.points
#         and T.PUNCTUATION_MAQAF in uni
#     ):
#         guess.vowel = T.NAME_QAMATS_QATAN
#         return guess


## `sheva`


@rule("sheva", r"sheva-na-start-word")
def sheva_na_start_word(isfirst, guess):
    """`sheva` at word start is `sheva-na`"""
    if isfirst and guess.vowel == T.NAME_SHEVA:
        guess.vowel = T.NAME_SHEVA_NA
        return guess


@rule("sheva", "sheva-nah-end-word")
def sheva_nah_end_word(islast, guess):
    """`sheva` at the end of a word is `sheva-nah`"""
    if islast and guess.vowel == T.NAME_SHEVA:
        guess.vowel = T.NAME_SHEVA_NAH
        guess.isopen = False
        return guess


@rule("sheva", "sheva-nah-alef-end-word")
def sheva_nah_alef_end(neg_idx, guess, next_guess):
    """`sheva` before last bare `alef` is `sheva-nah`"""
    if neg_idx == 1 and guess.vowel == T.NAME_SHEVA and next_guess.isbare(T.NAME_ALEF):
        guess.vowel = T.NAME_SHEVA_NAH
        next_guess.isopen = True
        return guess


@rule("sheva", "sheva-double-end")
def sheva_double_end(neg_idx, guess, next_guess):
    """two `sheva` at word end are `sheva-na`, `sheva-na`"""
    if (
        neg_idx == 1
        and guess.vowel == T.NAME_SHEVA
        and next_guess.vowel == T.NAME_SHEVA
    ):
        guess.vowel = T.NAME_SHEVA_NA
        next_guess.vowel = T.NAME_SHEVA_NA
        return guess


@rule("sheva", "sheva-double-middle")
def sheva_double_middle(neg_idx, guess, next_guess):
    """two `sheva` midword are `sheva-nah`, `sheva-na`"""
    if neg_idx > 1 and guess.vowel == T.NAME_SHEVA and next_guess.vowel == T.NAME_SHEVA:
        guess.vowel = T.NAME_SHEVA_NAH
        next_guess.vowel = T.NAME_SHEVA_NA
        return guess


@rule("sheva", "sheva-na-double-letter")
def sheva_na_double_letter(guess, next_guess):
    """`sheva` before same letter is `sheva-na`"""
    if guess.has(
        vowel=T.NAME_SHEVA, letter=next_guess.letter
    ) and not next_guess.vowel.startswith(T.NAME_SHEVA):
        guess.vowel = T.NAME_SHEVA_NA
        return guess


@rule("sheva", "sheva-na-dagesh-hazaq")
def sheva_na_dagesh_hazaq(guess):
    """`sheva` under `dagesh-hazaq` is `sheva-na`"""
    if guess.has(vowel=T.NAME_SHEVA, dagesh=T.NAME_DAGESH_HAZAQ):
        guess.vowel = T.NAME_SHEVA_NA
        return guess


@rule("sheva", "sheva-na-after-long-vowel")
def sheva_na_after_long_vowel(last_vowel, guess):
    """`sheva` after long vowel is `sheva-na`"""
    if guess.vowel == T.NAME_SHEVA and NIQQUD_LONG == niqqudtype(last_vowel):
        guess.vowel = T.NAME_SHEVA_NA
        return guess


@rule("sheva", "sheva-nah-after-short-vowel")
def sheva_nah_after_short_vowel(last_vowel, guess):
    """`sheva` after short vowel is `sheva-nah`"""
    if guess.vowel == T.NAME_SHEVA and niqqudtype(last_vowel) in [
        NIQQUD_SHORT,
        NIQQUD_HATAF,
    ]:
        guess.vowel = T.NAME_SHEVA_NAH
        return guess
