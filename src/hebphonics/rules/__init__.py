#!/usr/bin/env python
# coding: utf-8
"""Rules of Hebrew grammar.

The primary sources for these rules are:

- Even-Shoshan, Avraham. [_HaMillon Heḥadash_][HaMillon]. Jerusalem, 1961.
- Riachi, Shmuel Meir, ed. [_Tikkun Korim: Simanim_][Simanim]. Jerusalem, 1995.
- Khan, Geoffrey. [_The Tiberian Pronunciation Tradition of Biblical Hebrew, Volume I_][Khan]. Cambridge, UK, 2020.
- Gesenius, Wilhelm. [_Gesenius' Hebrew Grammar_][Gesenius]. Boston, 1839.
- [Wikipedia][Wikipedia-Niqqud]

See also:
[Gesenius]: https://babel.hathitrust.org/cgi/pt?id=mdp.39015008540497
[HaMillon]: https://opensiddur.org/wp-content/uploads/2017/08/Even-Shoshan-Diqduq.pdf
[Khan]: https://doi.org/10.11647/OBP.0163
[Simanim]: http://www.librarything.com/work/4905686
[Wikipedia-Dagesh]: https://en.wikipedia.org/wiki/Dagesh
[Wikipedia-Mapiq]: https://en.wikipedia.org/wiki/Mappiq
[Wikipedia-Niqqud]: https://en.wikipedia.org/wiki/Niqqud
[Wikipedia-Sheva]: https://en.wikipedia.org/wiki/Shva
"""

# native
from typing import Callable
from inspect import signature

# pkg
from .. import tokens as T

T_BEGEDKEFET = {
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

PREFIX_MORPHEMES = [
    T.NAME_BET,
    T.NAME_VET,
    T.NAME_VAV,
    T.NAME_KAF,
    T.NAME_KHAF,
    T.NAME_LAMED,
    T.NAME_TAV,
    T.NAME_SAV,
]

SONORORANT_LETTERS = [T.NAME_YOD, T.NAME_LAMED, T.NAME_MEM, T.NAME_NUN, T.NAME_RESH]


T_GLOTTAL_LETTERS = [T.LETTER_ALEF, T.LETTER_HE, T.LETTER_AYIN]


ALEF_HE = [T.NAME_ALEF, T.NAME_HE]
ALEF_HE_YOD = [T.NAME_ALEF, T.NAME_HE, T.NAME_YOD]

GUTTURAL_LETTERS = [T.NAME_ALEF, T.NAME_HE, T.NAME_HET, T.NAME_AYIN]
"""Letters the are pronounced deep in the throat (Source: [Simanim] 4.1)."""

NON_DAGESH_LETTERS = GUTTURAL_LETTERS + [T.NAME_RESH]
"""Letters which cannot receive a `dagesh-hazaq` (Source: [Simanim] 1.3)."""


SIMILAR_LETTERS = [
    (T.NAME_ALEF, T.NAME_MAPIQ_ALEF, T.NAME_AYIN),
    (T.NAME_VET, T.NAME_VAV),
    (T.NAME_DALET, T.NAME_TET, T.NAME_TAV),
    (T.NAME_HE, T.NAME_MAPIQ_HE),
    (T.NAME_HET, T.NAME_KHAF, T.NAME_KHAF_SOFIT),
    (T.NAME_KAF, T.NAME_KAF_SOFIT, T.NAME_QOF),
    (T.NAME_MEM, T.NAME_MEM_SOFIT),
    (T.NAME_NUN, T.NAME_NUN_SOFIT),
    (T.NAME_SAMEKH, T.NAME_SIN, T.NAME_SAV),
    (T.NAME_PE, T.NAME_PE_SOFIT),
    (T.NAME_FE, T.NAME_FE_SOFIT),
    (T.NAME_TSADI, T.NAME_TSADI_SOFIT),
]
"""Letters with the same sound or manner of articulation."""

NIQQUD_DAGESH = "dagesh"
NIQQUD_SHEVA = "sheva"
NIQQUD_HATAF = "hataf"
NIQQUD_LONG = "long"
NIQQUD_SHORT = "short"
NIQQUD_TYPES = {
    T.NAME_HATAF_SEGOL: NIQQUD_HATAF,
    T.NAME_HATAF_PATAH: NIQQUD_HATAF,
    T.NAME_HATAF_QAMATS: NIQQUD_HATAF,
    #
    T.NAME_HIRIQ: NIQQUD_SHORT,
    T.NAME_HIRIQ_MALE_YOD: NIQQUD_LONG,
    #
    T.NAME_TSERE: NIQQUD_LONG,
    # T.NAME_TSERE_MALE_ALEF: NIQQUD_LONG,
    # T.NAME_TSERE_MALE_HE: NIQQUD_LONG,
    # T.NAME_TSERE_MALE_YOD: NIQQUD_LONG,
    #
    T.NAME_SEGOL: NIQQUD_SHORT,
    # T.NAME_SEGOL_MALE_ALEF: NIQQUD_SHORT,
    # T.NAME_SEGOL_MALE_HE: NIQQUD_SHORT,
    # T.NAME_SEGOL_MALE_YOD: NIQQUD_SHORT,
    #
    T.NAME_PATAH: NIQQUD_SHORT,
    # T.NAME_PATAH_MALE_ALEF: NIQQUD_SHORT,
    # T.NAME_PATAH_MALE_HE: NIQQUD_SHORT,
    T.NAME_PATAH_GENUVAH: NIQQUD_SHORT,
    #
    T.NAME_QAMATS: NIQQUD_LONG,
    T.NAME_QAMATS_GADOL: NIQQUD_LONG,
    # T.NAME_QAMATS_MALE_ALEF: NIQQUD_LONG,
    # T.NAME_QAMATS_MALE_HE: NIQQUD_LONG,
    T.NAME_QAMATS_QATAN: NIQQUD_SHORT,
    #
    T.NAME_HOLAM: NIQQUD_LONG,
    T.NAME_HOLAM_HASER: NIQQUD_LONG,
    # T.NAME_HOLAM_MALE_ALEF: NIQQUD_LONG,
    # T.NAME_HOLAM_MALE_HE: NIQQUD_LONG,
    T.NAME_HOLAM_MALE_VAV: NIQQUD_LONG,
    #
    T.NAME_QUBUTS: NIQQUD_SHORT,
    T.NAME_SHURUQ: NIQQUD_LONG,
}
"""Categories of niqqud."""


def issimilar(letter1: str, letter2: str) -> bool:
    """Return True if two letters are considered similar.

    >>> issimilar(T.NAME_VET, T.NAME_VAV)
    True
    >>> issimilar(T.NAME_DALET, T.NAME_RESH)
    False
    """
    return letter1 == letter2 or any(
        [letter1 in x and letter2 in x for x in SIMILAR_LETTERS]
    )


def isvowel(point: str) -> bool:
    """Return True if the point name is a vowel.

    >>> isvowel(T.NAME_QAMATS)
    True
    """
    return NIQQUD_TYPES.get(point) in [NIQQUD_HATAF, NIQQUD_SHORT, NIQQUD_LONG]


def has_pattern(guesses, pattern):
    """Return True if `guesses` match `pattern`."""
    result = len(guesses) >= len(pattern)
    if result:
        for guess, check in zip(guesses, pattern):
            result = result and guess.has(**check)
            if not result:
                break
    return result


def has_sequence(idx, guesses, pattern, extra=0):
    """Return True if `guesses` has a run of `pattern`."""
    num = len(pattern) + extra
    return has_pattern(guesses[idx : idx + num], pattern)


def has_ending(neg_idx, guesses, pattern, extra=0):
    """Return True if `guesses` ends in `pattern`."""
    num = len(pattern) + extra
    at_position = neg_idx == num - 1
    return at_position and has_pattern(guesses[-num:], pattern)


RULES = {}

STAGES = {
    "vav": [],
    "dagesh": [],
    "eim-qria": [],
    "vowel": [],
    "qamats": [],
    "prefix": [],
    "sheva": [],
    "sheva2": [],
    "dagesh2": [],
    "qamats2": [],
}


def rule(stage, name) -> Callable:
    """Label a rule with a name."""

    def generator(original: Callable) -> Callable:
        original.rule = name
        original.params = list(signature(original).parameters)
        STAGES[stage].append(original)
        RULES[name] = original
        return original

    return generator


# NOTE: import all rules here to avoid circular import
# pylint: disable=wrong-import-position
from . import eim_qria, dagesh, vowel, qamats, sheva
