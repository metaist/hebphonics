#!/usr/bin/env python
# coding: utf-8
"""Unicode characters, code points, and Hebrew letters.

This module defines:
    - constants for Unicode characters for Hebrew (and Yiddish)
    - constants for the grammatical names of Hebrew characters
    - utility functions for getting character names and grammatical names

UNICODE NAMES
    The Unicode constants are named following the Unicode 6.1 standard
    with punctuation (spaces, dashes) replaced by underscores and the
    prefix `HEBREW ` removed (e.g., `HEBREW LETTER ALEF` becomes
    `LETTER_ALEF`).

GRAMMATICAL NAMES
    The grammatical names of the Hebrew characters differ from the standard
    Unicode name in that they refer to the grammatical function of the
    character rather than its presentation form. For example, Unicode does
    not distinguish between a `dagesh-qal` or a `dagesh-hazaq` where as
    we do.

CODE POINTS
    The following Unicode charts may be helpful in understanding the symbols used.
    - [C0 Controls and Basic Latin](https://www.unicode.org/charts/PDF/U0000.pdf)
    - [General Punctuation](https://www.unicode.org/charts/PDF/U2000.pdf)
    - [Hebrew](https://www.unicode.org/charts/PDF/U0590.pdf)
    - [Alphabetic Presentation Forms](https://www.unicode.org/charts/PDF/UFB00.pdf)
"""

# native
from typing import List
import re
import unicodedata

RE_CONST_REMOVE = re.compile(r"(^HEBREW )|[ -]")
RE_SHORT_REMOVE = re.compile(r"^(ACCENT|LETTER|LIGATURE|MARK|POINT|PUNCTUATION)_")
RE_LETTER_POINT = re.compile(r"^(LETTER|POINT)_")

normalize = lambda u: unicodedata.normalize("NFKD", u)
unicode_name = lambda u: unicodedata.name(u, f"U+{hex(ord(u)).replace('x', '')}")
const_name = lambda u: RE_CONST_REMOVE.sub("_", unicode_name(u)).lstrip("_")
short_name = lambda u: RE_SHORT_REMOVE.sub("", const_name(u))

# unicode names
CODEPOINTS = {
    const_name(chr(n)): chr(n)
    for n in (
        [
            # C0 Controls and Basic Latin <https://www.unicode.org/charts/PDF/U0000.pdf>
            0x0020,  # SPACE
            0x002F,  # SOLIDUS; used as morphological divider in Tanach
            # Combining Diacritical Marks <https://www.unicode.org/charts/PDF/U0300.pdf>
            0x034F,  # COMBINING GRAPHEME JOINER
            # General Punctuation <https://www.unicode.org/charts/PDF/U2000.pdf>
            0x200C,  # ZERO WIDTH NON-JOINER
            0x200D,  # ZERO WIDTH JOINER
            0x200E,  # LEFT-TO-RIGHT MARK
            0x200F,  # RIGHT-TO-LEFT MARK
        ]
        +
        # Hebrew <https://www.unicode.org/charts/PDF/U0590.pdf>
        list(range(0x0590, 0x05F4))
        +
        # Alphabet Presentation Forms <https://www.unicode.org/charts/PDF/UFB00.pdf>
        list(range(0xFB1D, 0xFB4F))
    )
    if unicodedata.name(chr(n), "")
}
"""Unicode symbols you may encounter when parsing Hebrew text."""

point = lambda n: CODEPOINTS.get(n, "")

HATAF_VOWELS = [
    point(p)
    for p in [
        "POINT_HATAF_SEGOL",
        "POINT_HATAF_PATAH",
        "POINT_HATAF_QAMATS",
    ]
]

VOWELS = [
    point(p)
    for p in [
        "POINT_SHEVA",
        "POINT_HIRIQ",
        "POINT_TSERE",
        "POINT_SEGOL",
        "POINT_PATAH",
        "POINT_QAMATS",
        "POINT_QAMATS_QATAN",
        "POINT_HOLAM",
        "POINT_HOLAM_HASER_FOR_VAV",
        "POINT_QUBUTS",
    ]
]

# grammatical names
SYMBOLS = {
    # dagesh
    "mapiq": point("POINT_DAGESH_OR_MAPIQ"),
    "dagesh": point("POINT_DAGESH_OR_MAPIQ"),  # uncategorized dagesh
    "dagesh-qal": point("POINT_DAGESH_OR_MAPIQ"),
    "dagesh-hazaq": point("POINT_DAGESH_OR_MAPIQ"),
    # sheva
    "sheva": point("POINT_SHEVA"),  # uncategorized sheva
    "sheva-na": point("POINT_SHEVA"),
    "sheva-na-mute": point("POINT_SHEVA"),  # modern Hebrew
    "sheva-nah": point("POINT_SHEVA"),
    "sheva-nah-voiced": point("POINT_SHEVA"),  # modern Hebrew
    "sheva-gaya": point("POINT_SHEVA") + point("POINT_METEG"),  # Yemenite
    # hiriq
    "hiriq": point("POINT_HIRIQ"),
    "hiriq-male-yod": point("POINT_HIRIQ"),
    # tsere
    "tsere": point("POINT_TSERE"),
    "tsere-male-alef": point("POINT_TSERE"),
    "tsere-male-he": point("POINT_TSERE"),
    "tsere-male-yod": point("POINT_TSERE"),
    # segol
    "segol": point("POINT_SEGOL"),
    "segol-male-alef": point("POINT_SEGOL"),
    "segol-male-he": point("POINT_SEGOL"),
    "segol-male-yod": point("POINT_SEGOL"),
    "hataf-segol": point("POINT_HATAF_SEGOL"),
    # patah
    "patah": point("POINT_PATAH"),
    "patah-male-alef": point("POINT_PATAH"),
    "patah-male-he": point("POINT_PATAH"),
    "patah-yod": point("POINT_PATAH"),
    "patah-genuvah": point("POINT_PATAH"),
    "hataf-patah": point("POINT_HATAF_PATAH"),
    # qamats
    "qamats": point("POINT_QAMATS"),  # unclassified qamats
    "qamats-gadol": point("POINT_QAMATS"),
    "qamats-male-alef": point("POINT_QAMATS"),
    "qamats-male-he": point("POINT_QAMATS"),
    "qamats-yod": point("POINT_QAMATS"),
    "qamats-yod-vav": point("POINT_QAMATS"),
    "hataf-qamats": point("POINT_HATAF_QAMATS"),
    "qamats-qatan": point("POINT_QAMATS_QATAN"),
    # holam
    "holam": point("POINT_HOLAM"),
    "holam-haser": point("POINT_HOLAM"),
    "holam-male-alef": point("POINT_HOLAM"),
    "holam-male-he": point("POINT_HOLAM"),
    "holam-male-vav": point("LETTER_VAV") + point("POINT_HOLAM"),
    # qubuts / shuruq
    "qubuts": point("POINT_QUBUTS"),
    "shuruq": point("LETTER_VAV") + point("POINT_DAGESH_OR_MAPIQ"),
    # Letters
    # NOTE: We call them "{x}-sofit" rather than "final-{x}".
    "alef": point("LETTER_ALEF"),
    "mapiq-alef": point("LETTER_ALEF"),
    "bet": point("LETTER_BET"),
    "vet": point("LETTER_BET"),
    "gimel": point("LETTER_GIMEL"),
    "dalet": point("LETTER_DALET"),
    "he": point("LETTER_HE"),
    "mapiq-he": point("LETTER_HE"),
    "vav": point("LETTER_VAV"),
    "zayin": point("LETTER_ZAYIN"),
    "het": point("LETTER_HET"),
    "tet": point("LETTER_TET"),
    "yod": point("LETTER_YOD"),
    "kaf": point("LETTER_KAF"),
    "kaf-sofit": point("LETTER_FINAL_KAF"),
    "khaf": point("LETTER_KAF"),
    "khaf-sofit": point("LETTER_FINAL_KAF"),
    "lamed": point("LETTER_LAMED"),
    "mem": point("LETTER_MEM"),
    "mem-sofit": point("LETTER_FINAL_MEM"),
    "nun": point("LETTER_NUN"),
    "nun-sofit": point("LETTER_FINAL_NUN"),
    "samekh": point("LETTER_SAMEKH"),
    "ayin": point("LETTER_AYIN"),
    "pe": point("LETTER_PE"),
    "pe-sofit": point("LETTER_FINAL_PE"),
    "fe": point("LETTER_PE"),
    "fe-sofit": point("LETTER_FINAL_PE"),
    "tsadi": point("LETTER_TSADI"),
    "tsadi-sofit": point("LETTER_FINAL_TSADI"),
    "qof": point("LETTER_QOF"),
    "resh": point("LETTER_RESH"),
    "shin": point("LETTER_SHIN") + point("POINT_SHIN_DOT"),
    "sin": point("LETTER_SHIN") + point("POINT_SIN_DOT"),
    "tav": point("LETTER_TAV"),
    "sav": point("LETTER_TAV"),
}
"""Grammatical symbols and how to convert them to Unicode symbols."""

locals().update(CODEPOINTS)
locals().update({f"NAME_{n.upper().replace('-', '_')}": n for n in SYMBOLS})


def uniname(char, ignore=True, mode="short"):
    """Returns the name of a Unicode code point.

    Args:
        char (unicode): unicode character

    Kwargs:
        ignore (bool): whether or not to exclude code points outside of
            HebPhonics (default: True)
        mode (str): one of:
            * 'unicode': return the full Unicode character name
            * 'const': return the HebPhonics constant name
            * 'short': (default) same as 'const', but without another prefix

    Returns:
        str. String name of the Unicode code point.

    Examples:
    >>> uniname(LETTER_ALEF, mode='const')
    'LETTER_ALEF'
    >>> [uniname(x, mode='const') for x in LETTER_ALEF + POINT_HIRIQ]
    ['LETTER_ALEF', 'POINT_HIRIQ']
    >>> [uniname(x, mode='short') for x in LETTER_ALEF + POINT_HIRIQ]
    ['ALEF', 'HIRIQ']

    Characters outside of HebPhonics can be allowed:
    >>> [uniname(x, mode='const') for x in LETTER_ALEF + u'\u00C1' if uniname(x)]
    ['LETTER_ALEF']
    >>> [uniname(x, ignore=False, mode='const') for x in LETTER_ALEF + u'\u00C1']
    ['LETTER_ALEF', 'LATIN_CAPITAL_LETTER_A_WITH_ACUTE']

    >>> uniname('') is None
    True
    """
    func = {"const": const_name, "short": short_name}.get(mode, unicode_name)
    return func(char) if char in CODEPOINTS.values() or not ignore else None


def strip(uni: str) -> str:
    """Returns the string with only letters and points.

    Args:
        uni (unicode): unicode string

    Returns:
        str. Cleaned string with only letters and points.

    Examples:
    >>> strip(LETTER_ALEF + POINT_PATAH) == LETTER_ALEF + POINT_PATAH
    True
    >>> strip(LETTER_ALEF + "/") == LETTER_ALEF
    True
    """
    result = []
    included = []
    excluded = ["POINT_METEG", "POINT_RAFE"]
    for token in uni:
        name = uniname(token, mode="const", ignore=False)
        if (
            name
            and (name not in excluded and RE_LETTER_POINT.match(name))
            or name in included
        ):
            result.append(token)
    return "".join(result)


def from_names(symbols: List[str]) -> str:
    """Return a string representation of the given grammatical symbols.

    >>> from_names(["shin", "qamats", "lamed", "holam-male-vav", "mem-sofit"]) == r"שָׁלוֹם"
    True
    """
    return "".join([SYMBOLS.get(s, "") for s in symbols])


def flatten(lst: List) -> list:
    """Reduce a nested list to a single flat list.

    >>> flatten(["A", [2, ["C"]], ["DE", (5, 6)]]) == ["A", 2, "C", "DE", 5, 6]
    True
    """
    result = []
    for item in lst:
        isiterable = False
        try:
            iter(item)
            isiterable = True
        except TypeError:
            pass

        if isiterable and not isinstance(item, str):
            result += flatten(item)
        else:
            result.append(item)
    return result
