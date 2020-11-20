#!/usr/bin/env python
# coding: utf-8
"""Hebrew grammar parsing.

This module provides basic functions for classifying Hebrew characters
(or sequences of characters) according to their grammatical function.

NOTE
    This is a "best-effort" parser and while attempts are made at correctness,
    some characters may be underspecified or incorrectly specified
    (e.g., "qamats" rather than "qamats-qatan").
"""

# native
from dataclasses import dataclass, field
from typing import List
import re

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

## Niqqud
NIQQUD_DAGESH = "dagesh"
NIQQUD_SHEVA = "sheva"
NIQQUD_HATAF = "hataf"
NIQQUD_LONG = "long"
NIQQUD_SHORT = "short"
NIQQUD_TYPES = {
    T.NAME_DAGESH: NIQQUD_DAGESH,
    T.NAME_DAGESH_HAZAQ: NIQQUD_DAGESH,
    T.NAME_DAGESH_QAL: NIQQUD_DAGESH,
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
    T.NAME_HIRIQ_MALE: NIQQUD_LONG,
    T.NAME_TSERE: NIQQUD_LONG,
    T.NAME_TSERE_MALE: NIQQUD_LONG,
    T.NAME_SEGOL: NIQQUD_SHORT,
    T.NAME_SEGOL_MALE: NIQQUD_SHORT,
    T.NAME_PATAH: NIQQUD_SHORT,
    T.NAME_PATAH_MALE: NIQQUD_SHORT,
    T.NAME_PATAH_GENUVAH: NIQQUD_SHORT,
    T.NAME_QAMATS: NIQQUD_LONG,
    T.NAME_QAMATS_MALE: NIQQUD_LONG,
    T.NAME_QAMATS_QATAN: NIQQUD_SHORT,
    T.NAME_HOLAM_MALE: NIQQUD_LONG,
    T.NAME_HOLAM_HASER: NIQQUD_LONG,
    T.NAME_QUBUTS: NIQQUD_SHORT,
    T.NAME_SHURUQ: NIQQUD_LONG,
}
"""Categories of niqqud."""


## Gematria
GEMATRIA_VALUES = {
    T.LETTER_ALEF: 1,
    T.LETTER_BET: 2,
    T.LETTER_GIMEL: 3,
    T.LETTER_DALET: 4,
    T.LETTER_HE: 5,
    T.LETTER_VAV: 6,
    T.LETTER_ZAYIN: 7,
    T.LETTER_HET: 8,
    T.LETTER_TET: 9,
    T.LETTER_YOD: 10,
    T.LETTER_KAF: 20,
    T.LETTER_FINAL_KAF: 20,
    T.LETTER_LAMED: 30,
    T.LETTER_MEM: 40,
    T.LETTER_FINAL_MEM: 40,
    T.LETTER_NUN: 50,
    T.LETTER_FINAL_NUN: 50,
    T.LETTER_SAMEKH: 60,
    T.LETTER_AYIN: 70,
    T.LETTER_PE: 80,
    T.LETTER_FINAL_PE: 80,
    T.LETTER_TSADI: 90,
    T.LETTER_FINAL_TSADI: 90,
    T.LETTER_QOF: 100,
    T.LETTER_RESH: 200,
    T.LETTER_SHIN: 300,
    T.LETTER_TAV: 400,
}
"""Numerical values of the Hebrew unicode letters."""

RE_SHEMOT = (
    "("
    + ")|(".join(
        [
            r"א(ֱ)?ל(ו)?ֹה",  # Shem Elokah
            r"א(.)?ד(ו)?ֹנ[ָ|ַ]י$",  # Shem Adnuth
            r"י(ּ)?(ְ|ֱ|ֲ)?ה(ֹ)?ו[ָ|ִ]ה",  # Shem HaVayah
            r"([^י]|^)שׁ[ַ|ָ]ד(ּ)?[ָ|ַ]י$",  # Shakai
            r"^אֵל(.)?$",  # Kel
            r"^יָהּ$",  # Kah
            r"^צְבָאוֹת$",  # Tzvakot
        ]
    )
    + ")"
)
"""Regex that matches the seven special names of G-d.

In Judaism, printing shem-haShem (name of G-d) carries additional
obligations and is often avoided.
"""


def gematria(uni: str) -> int:
    """Return the numerical value of a Hebrew string.

    Args:
        uni (unicode): unicode string

    Returns:
        int. numerical value of the string

    Examples:
    >>> gematria("שָׁלוֹם‎")
    376
    """
    return sum([GEMATRIA_VALUES[letter] for letter in uni if letter in GEMATRIA_VALUES])


def isshemot(uni: str) -> bool:
    """Returns True if the given unicode string contains a name of G-d.

    Args:
        uni (unicode): word to check

    Returns:
        bool. True if the word is a name of G-d.

    Examples:
    >>> isshemot("אֵל")
    True
    >>> isshemot("אֵלַי")
    False
    """
    return re.search(RE_SHEMOT, uni, re.I + re.U) is not None


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
    return NIQQUD_TYPES.get(T.hebname(point))


@dataclass
class Cluster:
    """Hebrew symbol cluster; a letter, dagesh, vowel, and points.

    Clusters are used both for lexing and for parsing. During lexing, the values
    are Unicode code points. During parsing, the values are the grammatical names
    of the symbols.
    """

    letter: str = None
    dagesh: str = None
    vowel: str = None
    points: List[str] = field(default_factory=list)

    def reset(self) -> "Cluster":
        """Reset the values of all the properties."""
        self.letter = None
        self.dagesh = None
        self.vowel = None
        self.points = []
        return self

    def __bool__(self) -> bool:
        """Return True if any part of the cluster is set.

        >>> bool(Cluster())
        False
        """
        return bool(self.letter or self.dagesh or self.vowel or self.points)

    def __len__(self) -> int:
        """Return number of items.

        >>> len(Cluster(letter='A', dagesh='B'))
        2
        """
        return len(self.tolist())

    def tolist(self) -> List[str]:
        """Returns a list representation of the cluster.

        >>> Cluster().tolist()
        []
        """
        return [
            item for item in [self.letter, self.dagesh, self.vowel] if item
        ] + self.points

    def append(self, point):
        """Adds a point to this cluster.

        >>> Cluster().append('Y').tolist()
        ['Y']
        """
        self.points.append(point)
        return self

    def update(self, letter=None, dagesh=None, vowel=None, points=None):
        """Sets the attributes of the cluster.

        >>> Cluster().update(letter='W', dagesh='X', vowel='Y', points=['Z']).tolist()
        ['W', 'X', 'Y', 'Z']
        """
        self.letter = letter or self.letter
        self.dagesh = dagesh or self.dagesh
        self.vowel = vowel or self.vowel
        self.points = points or self.points
        return self


class Parser:
    """Best-effort Hebrew language parser.

    Parsing is accomplished in three stages: lexing, parsing, fine-tuning.

    # Stage 1: Lexing
    In this stage, Unicode symbols are grouped together. The `Cluster` class is
    used to separate out the `letter` from any other `points` that might be nearby.

    # Stage 2: Parsing
    In this stage, we first approximate the grammatical symbol names from the
    Unicode symbol name. Then we apply a series of rules that discriminate between
    special cases. The flow is:
        - the `letter` is parsed with `parse_letter`
            - handle two letter-dependent `sheva` rules
            - separate `shuruq`, `vav` + `dagesh-hazaq`
            - separate `shin`, `sin`
            - process `dagesh-`
        - each of the `points` is parsed with `parse_vowel`
            - handle `patah-genuvah`
            - separate `holam-male`, `vav` + `holam-haser`
            - handle `qamats-qatan`
            - process `sheva-`

    # Stage 3: Fine-tuning
    While most parse rules only require the immediately preceding or current cluster
    of tokens, a few rules need to consider the state after almost all the other rules
    have been applied. For example, the final determination of `-male` vowels can
    depend on [_mater lectionis_][1] which may depend on a `shuruq` determiniation.

    [1]: https://en.wikipedia.org/wiki/Mater_lectionis
    """

    def __init__(self, uni: str):
        """Construct a new parser around a particular word."""
        self.uni = T.normalize(uni)
        self.lexed = self.lex(self.uni)
        self.parsed = []
        self.rules = []

    @staticmethod
    def lex(uni: str) -> List[Cluster]:
        """Return initial grouping of Unicode symbols."""
        lexed = []
        curr = Cluster()
        for symbol in uni:
            name = T.uniname(symbol, mode="const")
            if name.startswith("LETTER_"):
                if curr:  # add previous
                    lexed.append(curr)
                curr = Cluster(letter=symbol)
            elif symbol == T.POINT_DAGESH_OR_MAPIQ:
                curr.dagesh = T.NAME_DAGESH
            elif name.startswith("POINT_"):
                curr.append(symbol)
        if curr:  # add last
            lexed.append(curr)
        return lexed

    def parse_dagesh(
        self, token: Cluster, prev: Cluster, guess: Cluster, islast: bool = False
    ):
        """Apply `dagesh-` rules."""

        if T.LETTER_ALEF == token.letter and token.dagesh:
            # H101: `dagesh` in `alef` is `mapiq-alef` (dagesh-mapiq-alef)
            self.rules.append("H101")
            guess.update(letter=T.NAME_MAPIQ_ALEF, dagesh=T.NAME_MAPIQ)
        elif T.LETTER_HE == token.letter and token.dagesh:
            if islast:
                # H102: `dagesh` in last `he` is `mapiq-he` (dagesh-mapiq-he)
                self.rules.append("H102")
                guess.update(letter=T.NAME_MAPIQ_HE, dagesh=T.NAME_MAPIQ)
            else:
                # H103: `dagesh` in non-last `he` is `dagesh-hazaq` (dagesh-hazaq-he)
                self.rules.append("H103")
                guess.update(dagesh=T.NAME_DAGESH_HAZAQ)
        elif token.letter in BEGEDKEFET:
            name, changed = BEGEDKEFET[token.letter]
            guess.letter = name
            if token.dagesh and isvowel(prev.vowel):
                # H104: `dagesh` in BGDKFT after vowel is `dagesh-hazaq` (dagesh-hazaq-bgdkft)
                self.rules.append("H104")
                guess.update(letter=changed, dagesh=T.NAME_DAGESH_HAZAQ)
            elif token.dagesh:
                # H105: `dagesh` in BGDKFT NOT after vowel is `dagesh-qal` (dagesh-qal-bgdkft)
                # (including start of word)
                self.rules.append("H105")
                guess.update(letter=changed, dagesh=T.NAME_DAGESH_QAL)

        if T.NAME_DAGESH == guess.dagesh:
            # H106: any other `dagesh` is a `dagesh-hazaq` (dagesh-hazaq-other)
            self.rules.append("H106")
            guess.dagesh = T.NAME_DAGESH_HAZAQ

    def parse_letter(self, token: Cluster, guess: Cluster, islast: bool = False):
        """Update `guess` using letter-based rules.

        NOTE: May also modify immediately preceding parsed value.

        Args:
            token (Cluster): cluster of unparsed tokens
            guess (Cluster): semi-parsed tokens
            islast (bool): whether this is the last group of tokens
        """
        prev = self.parsed[-1] if self.parsed else Cluster()
        isfirst = not prev
        isbare = not token.dagesh and not token.points

        if (
            prev.letter == guess.letter
            and prev.vowel
            and prev.vowel.startswith(T.NAME_SHEVA)
        ):
            # H207: `sheva` before same letter is `sheva-na` (sheva-na-double-letter)
            self.rules.append("H207")
            prev.vowel = T.NAME_SHEVA_NA
        elif (
            T.LETTER_ALEF == token.letter
            and islast
            and isbare
            and prev.vowel
            and prev.vowel.startswith(T.NAME_SHEVA)
        ):
            # H206: `sheva` before last bare `alef` is `sheva-nah` (sheva-nah-alef-end)
            self.rules.append("H206")
            prev.vowel = T.NAME_SHEVA_NAH
        elif T.LETTER_VAV == token.letter and token.dagesh:
            if isfirst or not isvowel(prev.vowel):
                # H604: `VAV` with `DAGESH` NOT after vowel is `shuruq` (vav-is-shurug)
                self.rules.append("H604")
                guess.reset()  # reset guess
                (prev or guess).vowel = T.NAME_SHURUQ
            else:
                # H605: `VAV` with `DAGESH` after/has vowel is `vav`, `dagesh-hazaq` (vav-dagesh-hazaq)
                self.rules.append("H605")
                guess.dagesh = T.NAME_DAGESH_HAZAQ
        elif T.LETTER_SHIN == token.letter:
            name = T.NAME_SIN  # to handle Yissacher
            if T.POINT_SHIN_DOT in token.points:
                name = T.NAME_SHIN
            elif T.POINT_SIN_DOT in token.points:
                name = T.NAME_SIN
            guess.letter = name

        self.parse_dagesh(token, prev, guess, islast)

    def parse_sheva(self, prev: Cluster, guess: Cluster, islast: bool = False):
        """Apply `sheva-` rules."""
        isfirst = not prev
        prev_sheva = prev.vowel and prev.vowel.startswith(T.NAME_SHEVA)
        last_vowel = prev.vowel
        if not last_vowel and len(self.parsed) >= 2:
            last_vowel = self.parsed[-2].vowel

        if isfirst:
            # H201: `sheva` at word start is `sheva-na` (sheva-na-word-start)
            self.rules.append("H201")
            guess.vowel = T.NAME_SHEVA_NA
        elif islast and prev_sheva:
            # H209: two `sheva` at word end are `sheva-na`, `sheva-na` (sheva-double-end)
            self.rules.append("H209")
            prev.vowel = T.NAME_SHEVA_NA
            guess.vowel = T.NAME_SHEVA_NA
        elif islast:
            # H202: `sheva` at the end of a word is `sheva-nah` (sheva-nah-word-end)
            self.rules.append("H202")
            guess.vowel = T.NAME_SHEVA_NAH
        elif T.NAME_DAGESH_HAZAQ == guess.dagesh:
            # H203: `sheva` under `dagesh-hazaq` is `sheva-na` (sheva-na-dagesh-hazaq)
            self.rules.append("H203")
            guess.vowel = T.NAME_SHEVA_NA
        elif NIQQUD_LONG == niqqudtype(last_vowel):
            # H204: `sheva` after long vowel is `sheva-na` (sheva-na-after-long-vowel)
            self.rules.append("H204")
            guess.vowel = T.NAME_SHEVA_NA
        elif niqqudtype(last_vowel) in [NIQQUD_SHORT, NIQQUD_HATAF]:
            # H205: `sheva` after short vowel is `sheva-nah` (sheva-nah-after-short-vowel)
            self.rules.append("H205")
            guess.vowel = T.NAME_SHEVA_NAH
        elif prev_sheva:
            # H208: two `sheva` midword are `sheva-nah`, `sheva-na` (sheva-double-midword)
            self.rules.append("H207")
            prev.vowel = T.NAME_SHEVA_NAH
            guess.vowel = T.NAME_SHEVA_NA

    def parse_vowel(self, point: str, guess: Cluster, islast: bool = False):
        """Update `guess` using the vowel information.

        NOTE: May also modify immediately preceding parsed value.

        Args:
            point (str): vowel being processed
            guess (Cluster): currently parsed item
            islast (bool): whether this is the last token
        """
        prev = self.parsed[-1] if self.parsed else Cluster()

        if T.POINT_PATAH == point and islast:
            # H401: `patah` on last `het|ayin|mapiq-he` is `patah-genuvah` (patah-genuvah)
            self.rules.append("H401")  # NOTE: we don't actually check the letter
            guess.vowel = T.NAME_PATAH_GENUVAH
        elif T.POINT_HOLAM_HASER_FOR_VAV == point:
            # H601: `VAV` followed by `HOLAM_HASER_FOR_VAV` is `vav`, `holam-haser` (vav-holam-haser-unicode)
            self.rules.append("H601")
            guess.vowel = T.NAME_HOLAM_HASER
        elif T.POINT_HOLAM == point:
            guess.vowel = T.NAME_HOLAM_HASER
            if T.NAME_VAV == guess.letter:
                if not guess.dagesh and not prev.vowel:
                    # H602: `vav`, `HOLAM_HASER` NOT after vowel or sheva is `holam-male` (vav-is-holam-male)
                    self.rules.append("H602")
                    guess.reset()
                    (prev or guess).vowel = T.NAME_HOLAM_MALE
                else:
                    # H603: `VAV` with `HOLAM_HASER` after vowel or sheva `vav`, `holam-haser` (vav-holam-haser)
                    self.rules.append("H603")
                    guess.vowel = T.NAME_HOLAM_HASER
        elif T.POINT_QAMATS == point and T.PUNCTUATION_MAQAF in self.uni:
            # H502: `qamats` in non-last word with `maqaf` is `qamats-qatan` (qq-maqaf)
            self.rules.append("H502")
            guess.vowel = T.NAME_QAMATS_QATAN
        elif T.POINT_HATAF_QAMATS == point and prev and T.NAME_QAMATS == prev.vowel:
            # H503: `qamats` before `hataf-qamats` is `qamats-qatan` (qq-hataf-qamats)
            self.rules.append("H503")
            prev.vowel = T.NAME_QAMATS_QATAN
        elif T.POINT_SHEVA == point:
            self.parse_sheva(prev, guess, islast)

    def parse_male(self, prev: Cluster, guess: Cluster):
        """Apply `-male` rules."""
        if guess.dagesh or guess.vowel:
            return

        if T.NAME_HIRIQ == prev.vowel and T.NAME_YOD == guess.letter:
            # H301: `hiriq` before bare `yod` is `hiriq-male` (male-hiriq)
            self.rules.append("H301")
            prev.vowel = T.NAME_HIRIQ_MALE
        elif T.NAME_TSERE == prev.vowel and guess.letter in ALEF_HE_YOD:
            # H302: `tsere` before bare `alef|he|yod` is `tsere-male` (male-tsere)
            self.rules.append("H302")
            prev.vowel = T.NAME_TSERE_MALE
        elif T.NAME_SEGOL == prev.vowel and guess.letter in ALEF_HE_YOD:
            # H303: `segol` before bare `alef|he|yod` is `segol-male` (male-segol)
            self.rules.append("H303")
            prev.vowel = T.NAME_SEGOL_MALE
        elif T.NAME_PATAH == prev.vowel and guess.letter in ALEF_HE:
            # H304: `patah` before bare `alef|he` is `patah-male` (male-patah)
            self.rules.append("H304")
            prev.vowel = T.NAME_PATAH_MALE
        elif T.NAME_QAMATS == prev.vowel and guess.letter in ALEF_HE:
            # H305: `qamats` before bare `alef|he` is `qamats-male` (male-qamats)
            self.rules.append("H305")
            prev.vowel = T.NAME_QAMATS_MALE
        elif T.NAME_HOLAM_HASER == prev.vowel and guess.letter in ALEF_HE:
            # H306: `holam` before bare `alef|he` is `holam-male` (male-holam)
            self.rules.append("H306")
            prev.vowel = T.NAME_HOLAM_MALE

    def parse(self):
        """Return list of grammatical symbol names."""
        num = len(self.lexed)
        for i, token in enumerate(self.lexed):
            islast = i == num - 1

            letter = T.uniname(token.letter).lower()
            if letter.startswith("final_"):
                letter = f"{letter[6:]}-sofit"

            vowel = None
            if token.points:  # guess vowel name
                vowel = T.uniname(token.points[0]).lower().replace("_", "-")
                if not niqqudtype(vowel):
                    vowel = None

            guess = Cluster(letter=letter, dagesh=token.dagesh, vowel=vowel)
            self.parse_letter(token, guess, islast)
            for point in token.points:
                self.parse_vowel(point, guess, islast)

            if guess:
                self.parsed.append(guess)

        for i in range(len(self.parsed) - 1):
            self.parse_male(self.parsed[i], self.parsed[i + 1])

        return [name for group in self.parsed for name in group.tolist()]

    def syllabify(self, strict=False):
        """Returns a list of syllables.

        Kwargs:
            strict (bool): if True, follow rules of havarot (default: False)

        Returns:
            list<list<str>>. List of syllables (a lists of strings).
        """
        result, syllable = [], []
        syllable_break, last_vowel = False, ""

        for group in self.parsed:
            syllable_break = False

            if isvowel(group.vowel):
                # H001: syllable break before a vowel
                self.rules.append("H001")
                syllable_break = True
            elif T.NAME_SHEVA_NA == group.vowel or T.NAME_SHEVA_NA == last_vowel:
                # H002: syllable break before and after `sheva-na`
                self.rules.append("H002")
                syllable_break = True

            if strict and NIQQUD_HATAF == niqqudtype(last_vowel):
                # H003: (strict) no syllable break after hataf-vowel
                self.rules.append("H003")
                syllable_break = False

            if syllable and syllable_break:
                result.append(syllable)
                syllable = []

            syllable += group.tolist()
            last_vowel = group.vowel or ""

        # iterated through all groups

        if syllable:  # add the last syllable
            result.append(syllable)

        return result
