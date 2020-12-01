#!/usr/bin/env python
# coding: utf-8
"""Hebrew grammar parsing.

This module provides basic functions for classifying Hebrew characters
(or sequences of characters) according to their grammatical function.

NOTE
    This is a "best-effort" parser and while attempts are made at correctness,
    some characters may be under-specified or incorrectly specified
    (e.g., "qamats" rather than "qamats-qatan").
"""

# native
from dataclasses import dataclass, field
from typing import Any, Iterable, List, Iterator, Union
import operator
import re

# pkg
from . import tokens as T
from .rules import STAGES, isvowel, NIQQUD_TYPES, NIQQUD_HATAF

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

RE_SHEMOT = re.compile(
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
    + ")",
    re.I + re.U,
)
"""Regex that matches the seven special names of G-d.

In Judaism, printing shem-haShem (name of G-d) carries additional
obligations and is often avoided.
"""


def gematria(uni: str) -> int:
    """Return the numerical value of a Hebrew string.

    >>> gematria("שָׁלוֹם")
    376
    """
    return sum([GEMATRIA_VALUES.get(letter, 0) for letter in uni])


def isshemot(uni: str) -> bool:
    """Returns True if the given unicode string contains a name of G-d.

    >>> isshemot("אֵל")
    True
    >>> isshemot("אֵלַי")
    False
    """
    return RE_SHEMOT.search(uni) is not None


class ItemList(list):
    """Like `list` except that properties come from the contents.

    >>> l = ItemList([Cluster(letter="A"), Token(letter="B")])
    >>> l.letter == ["A", "B"]
    True
    >>> l.attr(["letter"]) == ["A", "B"]
    True
    >>> l.attr(["letter"], first=True) == "A"
    True
    """

    def __getattr__(self, name) -> list:
        """Return a list of the this attribute in the contained atoms."""
        return self.attr(name, first=False)

    def attr(self, attrs, first=False) -> Union[Any, Iterable[Any]]:
        """Return the attribute value of the contained atoms.

        Args:
            attrs (list[str]): attributes to extract
            first (bool): get first value or None if there are none (default: False)

        Returns:
            (Any or list[Any]): the values of the attribute
        """
        if isinstance(attrs, str):
            attrs = [attrs]

        key = operator.attrgetter(*attrs)
        if first:  # short-circuit
            return key(self[0]) if self else None

        result = ItemList([key(item) for item in self])
        return result

    def flat(self) -> "ItemList":
        """Return a flattened version of this object."""
        return ItemList(T.flatten(self))


@dataclass
class BaseToken:
    """Base class for tokens and clusters."""

    letter: str = ""
    dagesh: str = ""
    vowel: str = ""

    @property
    def items(self) -> list:
        """Return the contents as a list."""
        return [item for item in [self.letter, self.dagesh, self.vowel] if item]

    def __bool__(self) -> bool:
        """Return True if any component is non-empty."""
        return bool(self.letter or self.dagesh or self.vowel)

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the items."""
        return iter(self.items)

    def __len__(self) -> int:
        """Return length of items."""
        return len(self.items)

    def has(self, **kwargs):
        """Return True if the token has the attributes listed."""
        result = True
        for prop, want in kwargs.items():
            have = getattr(self, prop, "")
            if not want or isinstance(want, bool):
                result = result and bool(have) == bool(want)
            elif isinstance(want, (tuple, list, dict)):
                result = result and have in want
            else:
                result = result and have == want
            if not result:
                break
        return result

    def isbare(self, letters) -> bool:
        """Return True if the token lacks a dagesh or vowel.

        >>> BaseToken(letter="A").isbare("A")
        True
        """
        return self.has(dagesh="", vowel="", letter=letters)


@dataclass
class Token(BaseToken):
    """Unicode code points grouped by role.

    >>> t = Token(letter="A", dagesh="B", points=["C", "D"])
    >>> list(t) == ["A", "B", "C", "D"]
    True
    >>> str(t) == "ABCD"
    True
    """

    points: List[str] = field(default_factory=list)
    accents: List[str] = field(default_factory=list)
    puncta: List[str] = field(default_factory=list)

    @property
    def items(self) -> list:
        """Return the contents as a list."""
        return (
            ([self.letter] if self.letter else [])
            + ([self.dagesh] if self.dagesh else [])
            + ([self.vowel] if self.vowel else [])
            + self.points
            + self.accents
            + self.puncta
        )

    def __bool__(self) -> bool:
        """Return True if any component is non-empty."""
        return bool(
            self.letter
            or self.dagesh
            or self.vowel
            or self.points
            or self.accents
            or self.puncta
        )

    def __str__(self) -> str:
        """Return a string representation."""
        return "".join(self.items)

    def isbare(self, letters=None) -> bool:
        """Return True if the cluster lacks a dagesh or points.

        >>> Token().isbare()
        True
        >>> Token(letter="A").isbare("A")
        True
        """
        result = not self.dagesh and not self.points
        if letters:
            result = result and self.letter in letters
        return result


@dataclass
class Cluster(BaseToken):
    """Grammatical cluster of a letter, dagesh, and vowel."""

    isopen: bool = False
    rules: List[str] = field(default_factory=ItemList)

    def reset(self) -> "Cluster":
        """Reset the values of all the properties."""
        return self.update(
            letter="", dagesh="", vowel="", isopen=False, rules=ItemList()
        )

    def update(self, **kwargs) -> "Cluster":
        """Sets the attributes of the cluster."""
        self.__dict__.update(kwargs)
        return self


class ParseError(Exception):
    """Indicates a problem during parsing."""


class Parser:
    """Best-effort Hebrew language parser.

    Stages:
      - **Grouping**: Unicode symbols are are grouped together using the `Cluster`
        class to separate out the `letter` from any `points`, `accents`, or other
        `puncta`.

      - **Initial Guess**: We use the Unicode symbol names to make an initial guess
        of the `letter` and `vowel` names.

      - **Letters & Dagesh**: We make final `letter` and `dagesh` determinations for
        `vav`, `mapiq-`, and `BGDKFT` letters.

      - **Vowels & Sheva**: We make final `vowel` determinations including
        `qamats-`, `male-`, and `sheva-`.
    """

    STAGE_ORDER = [["vav", "dagesh"], ["male", "vowel", "sheva"], ["last"]]

    def __init__(self, enabled: List[str] = None, disabled: List[str] = None):
        """Construct a new parser with certain rules enabled or disabled."""
        self.enabled = enabled or []
        self.disabled = disabled or []
        self.stages = {
            name: [fn for fn in funcs if self.allow(fn.rule)]
            for name, funcs in STAGES.items()
        }
        self.rules = [[self.stages.get(n, []) for n in ns] for ns in Parser.STAGE_ORDER]

    def allow(self, name: str, cluster: Cluster = None) -> bool:
        """Return True if the given rule is allowed."""
        allow = True
        if name in self.disabled:
            allow = False
        elif name in self.enabled:
            allow = True
        if allow and cluster:
            cluster.rules.append(name)
        return allow

    @staticmethod
    def lex(uni: str) -> List[Token]:
        """Return list of grouped Unicode tokens."""
        # pylint: disable=too-many-branches
        lexed = ItemList()
        token = Token()
        for symbol in uni:
            name = T.uniname(symbol, mode="const")
            if not name:
                msg = f"Cannot lex symbol {T.unicode_name(symbol)} in word: >>{uni}<<"
                raise ParseError(msg)

            category = name.split("_", 1)[0]
            if category == "LETTER":
                if token.letter:  # add previous
                    lexed.append(token)
                    token = Token(letter=symbol)
                else:  # in case accent came before the letter
                    token.letter = symbol
            elif symbol in [T.POINT_SHIN_DOT, T.POINT_SIN_DOT]:
                token.letter += symbol
            elif T.POINT_DAGESH_OR_MAPIQ == symbol:
                token.dagesh = symbol
            elif symbol in T.VOWELS + T.HATAF_VOWELS:
                token.vowel = symbol
            elif category == "POINT":
                token.points.append(symbol)
            elif category == "ACCENT":
                token.accents.append(symbol)
            else:  # MARK, PUNCTUATION
                token.puncta.append(symbol)

        if token:  # add last
            if not token.letter:
                msg = f"No letter in token {token!r} in word: >>{uni}<<"
                raise ParseError(msg)

            lexed.append(token)
        return lexed

    @staticmethod
    def guess(token: Token) -> Cluster:
        """Return an initial guess from a token."""
        dagesh = T.NAME_DAGESH if token.dagesh else ""

        letter = T.uniname(token.letter[0]).lower()
        if letter.startswith("final_"):
            letter = f"{letter[6:]}-sofit"
        if T.LETTER_SHIN in token.letter:
            letter = T.NAME_SHIN if T.POINT_SHIN_DOT in token.letter else T.NAME_SIN

        vowel = (T.uniname(token.vowel) or "").lower().replace("_", "-")
        if T.POINT_HOLAM_HASER_FOR_VAV == token.vowel:
            vowel = T.NAME_HOLAM_HASER
        return Cluster(letter, dagesh, vowel, isopen=bool(vowel))

    def parse(self, uni: str) -> List[Cluster]:
        """Return list of parsed cluster."""
        # pylint: disable=too-many-locals
        parsed = ItemList()
        tokens = self.lex(T.normalize(uni))
        guesses = [self.guess(token) for token in tokens]

        last_idx = len(tokens) - 1
        has_maqaf = uni and uni[-1] == T.PUNCTUATION_MAQAF
        for group_num, group in enumerate(self.rules):
            prev2, prev1 = Cluster(), Cluster()
            for idx, token in enumerate(tokens):
                guess = guesses[idx]
                if not guess:  # it was reset
                    continue

                islast = idx == last_idx
                context = dict(
                    idx=idx,
                    neg_idx=last_idx - idx,
                    has_maqaf=has_maqaf,
                    isfirst=idx == 0,
                    islast=islast,
                    prev=prev1,
                    token=token,
                    guess=guess,
                    guesses=guesses,
                    next_token=tokens[idx + 1] if not islast else Token(),
                    next_guess=guesses[idx + 1] if not islast else Cluster(),
                )

                for rules in group:
                    for fn in rules:
                        context["last_vowel"] = prev1.vowel or prev2.vowel
                        modified = fn(
                            **{k: v for k, v in context.items() if k in fn.params}
                        )
                        if modified:
                            modified.rules.append(fn.rule)
                            break

                prev2, prev1 = prev1, guess
                if group_num == 0:
                    parsed.append(guess)
        return parsed

    @staticmethod
    def syl(parsed: List[Cluster]) -> List[List[Cluster]]:
        """Return parsed clusters grouped by syllable."""
        result, syllable = [], []
        syllable_break, last_vowel = False, ""
        for group in parsed:
            syllable_break = False

            if isvowel(group.vowel):
                # syllable break before a vowel
                syllable_break = True
            elif group.vowel.startswith(T.NAME_SHEVA_NAH):
                # no syllable break before `sheva-nah`
                syllable_break = False

            if syllable and syllable_break:
                result.append(syllable)
                syllable = []

            syllable.append(group)
            last_vowel = group.vowel
        # iterated through all groups
        if syllable:  # add the last syllable
            result.append(syllable)
        return result

    @staticmethod
    def syllabify(parsed: List[Cluster], strict: bool = False):
        """Returns a list of syllables.

        Kwargs:
            strict (bool): if True, follow rules of havarot (default: False)

        Returns:
            list[list[str]]. List of syllables (a lists of strings).
        """
        result, syllable = [], []
        syllable_break, last_vowel = False, ""

        for group in parsed:
            syllable_break = False

            if isvowel(group.vowel):
                # H001: syllable break before a vowel
                # self.rules.append("H001")
                # if self.allow("syllable-before-vowel", group):
                syllable_break = True
            elif T.NAME_SHEVA_NA == group.vowel or T.NAME_SHEVA_NA == last_vowel:
                # H002: syllable break before and after `sheva-na`
                # self.rules.append("H002")
                # if self.allow("syllable-around-sheva-na", group):
                syllable_break = True
            if strict and NIQQUD_HATAF == NIQQUD_TYPES.get(last_vowel):
                # H003: (strict) no syllable break after hataf-vowel
                # self.rules.append("H003")
                # if self.allow("no-syllable-after-hataf", group):
                syllable_break = False

            if syllable and syllable_break:
                result.append(syllable)
                syllable = []

            syllable += list(group)
            last_vowel = group.vowel

        # iterated through all groups

        if syllable:  # add the last syllable
            result.append(syllable)

        return result
