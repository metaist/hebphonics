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
import re
import unicodedata

# unicode names
RE_CONST_REMOVE = re.compile(r"(^HEBREW )|[ -]")
RE_SHORT_REMOVE = re.compile(r"^(ACCENT|LETTER|LIGATURE|MARK|POINT|PUNCTUATION)_")
RE_LETTER_POINT = re.compile(r"^(LETTER|POINT)_")

normalize = lambda u: unicodedata.normalize("NFKD", u)
unicode_name = lambda u: unicodedata.name(u, f"U+{hex(ord(u)).replace('x', '')}")
const_name = lambda u: RE_CONST_REMOVE.sub("_", unicode_name(u)).lstrip("_")
short_name = lambda u: RE_SHORT_REMOVE.sub("", const_name(u))

UNICODE_POINTS = [
    chr(n)
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
]
"""Unicode symbols you may encounter when parsing Hebrew text."""

# grammatical names
F_SOFIT = lambda n: fr"(final-{n})|({n}-sofit)?"
RE_HATAF = r"c?hataf-"
RE_MALE = r"-malei?"
RE_MAPIQ = r"mapi[kq]-"
RE_SHEVA = r"she?va"
RE_HIRIQ = r"(ch|h)iri[kq]"
RE_TSERE = r"t[sz]erei?"
RE_SEGOL = r"segg?ol"
RE_PATAH = r"patac?h"
RE_QAMATS = r"[kq]amat[sz]"
RE_HOLAM = r"c?hol[ao]m"

GRAMMAR_NAMES = {
    name: re.compile(fr"^{regex}$")
    for name, regex in {
        # # punctuation
        # "meteg": r"(meteg|silu[kq])",
        # "rafe": r"rafe",
        # "maqaf": r"ma[kq]a(ph|f)",
        #
        # dagesh
        "mapiq": r"(mapi[kq])",
        "dagesh": r"(dagesh|shuri[kq])",  # an unclassified dagesh
        "dagesh-qal": r"dagesh-([kq]al|lene)",
        "dagesh-hazaq": r"dagesh-(c?haza[kq]|forte)",
        # sheva
        "sheva": RE_SHEVA,  # an unclassified sheva
        "sheva-na": RE_SHEVA + r"-na",
        "sheva-nah": RE_SHEVA + r"-nac?h",
        # hiriq
        "hiriq": RE_HIRIQ,
        "hiriq-male": RE_HIRIQ + RE_MALE,  # hiriq + yod
        # tsere
        "tsere": RE_TSERE,
        "tsere-male": RE_TSERE + RE_MALE,  # tsere + (alef|he|yod)
        # segol
        "segol": RE_SEGOL,
        "segol-male": RE_SEGOL + RE_MALE,  # segol + (alef|he|yod)
        "hataf-segol": RE_HATAF + RE_SEGOL,
        # patah
        "patah": RE_PATAH,
        "patah-male": RE_PATAH + RE_MALE,  # patah + (alef|he)
        "patah-genuvah": r"(furtive-)?" + RE_PATAH + r"(-g[ae]nuv(ah)?)?",
        "hataf-patah": RE_HATAF + RE_PATAH,
        # qamats
        "qamats": RE_QAMATS + r"(-gadol)?",
        "qamats-male": RE_QAMATS + RE_MALE,  # qamats + (alef|he)
        "hataf-qamats": RE_HATAF + RE_QAMATS,
        "qamats-qatan": RE_QAMATS + r"-([kq]atan|c?hatuf)",
        # holam
        "holam-male": RE_HOLAM + RE_MALE,  # holam + (alef|he|vav)
        "holam-haser": RE_HOLAM + r"(-c?haser)?",
        # qubuts / shuruq
        "qubuts": r"[kq]ubut[sz]",
        "shuruq": r"shur[eu][kq]",
        # Letters
        # NOTE: We call them "{x}-sofit" rather than "final-{x}".
        "alef": r"ale(f|ph)",
        "mapiq-alef": RE_MAPIQ + r"ale(f|ph)",
        "bet": r"bet",
        "vet": r"vet",
        "gimel": r"gimm?el",
        "dalet": r"dalet",
        "he": r"hey?",
        "mapiq-he": RE_MAPIQ + r"hey?",
        "vav": r"vav",
        "zayin": r"zayin",
        "het": r"c?het",
        "tet": r"tet",
        "yod": r"y[ou]d",
        "kaf": r"kaf",
        "kaf-sofit": F_SOFIT(r"kaf"),
        "khaf": r"[kc]haf",
        "khaf-sofit": F_SOFIT(r"[kc]haf"),
        "lamed": r"lamed",
        "mem": r"mem",
        "mem-sofit": F_SOFIT(r"mem"),
        "nun": r"nun",
        "nun-sofit": F_SOFIT(r"nun"),
        "samekh": r"same[ck]h",
        "ayin": r"ayin",
        "pe": r"pey?",
        "pe-sofit": F_SOFIT(r"pey?"),
        "fe": r"fey?",
        "fe-sofit": F_SOFIT(r"fey?"),
        "tsadi": r"t[sz]adi",
        "tsadi-sofit": F_SOFIT(r"t[sz]adi"),
        "qof": r"[kq][ou]f",
        "resh": r"rei?sh",
        "shin": r"shin",
        "sin": r"sin",
        "tav": r"ta[fv]",
        "sav": r"sa[fv]",
    }.items()
}

locals().update({const_name(c): c for c in UNICODE_POINTS if unicodedata.name(c, "")})
locals().update({f"NAME_{n.upper().replace('-', '_')}": n for n in GRAMMAR_NAMES})


def strip(uni: str) -> str:
    """Returns the string with only letters and points.

    Args:
        uni (unicode): unicode string

    Returns:
        str. Cleaned string with only letters and points.

    Examples:
    >>> strip(LETTER_ALEF) == LETTER_ALEF
    True
    >>> strip(LETTER_ALEF + POINT_PATAH) == LETTER_ALEF + POINT_PATAH
    True
    >>> strip(LETTER_ALEF + POINT_PATAH + PUNCTUATION_MAQAF) == (LETTER_ALEF +
    ...     POINT_PATAH)
    True
    """
    result = []
    # print(uni, [uniname(t, mode="const", ignore=False) for t in uni])
    excluded = ["POINT_METEG", "POINT_RAFE"]
    for token in uni:
        name = uniname(token, mode="const", ignore=False)
        if name and name not in excluded and RE_LETTER_POINT.match(name):
            result.append(token)
    return "".join(result)


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
    return func(char) if char in UNICODE_POINTS or not ignore else None


def hebname(name):
    """Return the normalized HebPhonics name for a Hebrew charachter.

    Args:
        name (str): character name

    Returns:
        str. normalized name

    Normalization is is case-insensitive:
    >>> hebname('shva')
    'sheva'
    >>> hebname('sHeVa')
    'sheva'

    If the name is not known, the result is ``None``:
    >>> hebname('unknown-name') is None
    True

    The normalized name generally follows the Unicode spelling:
    >>> hebname('aleph')
    'alef'
    >>> hebname('alef')
    'alef'
    >>> hebname('yud')
    'yod'
    >>> hebname('kuf')
    'qof'
    >>> hebname('kamatz')
    'qamats'

    Final letters which are named with a "-sofit" suffix rather than a
    "final-" prefix:
    >>> hebname('final-mem')
    'mem-sofit'
    >>> hebname('kaf-sofit')
    'kaf-sofit'

    HebPhonics is also aware of names that refer to grammatical constructs and
    multi-character symbols:
    >>> hebname('dagesh-chazak')
    'dagesh-hazaq'
    >>> hebname('shva-nach')
    'sheva-nah'
    >>> hebname('patach-ganuvah')
    'patah-genuvah'
    >>> hebname('mapiq-hey')
    'mapiq-he'

    >>> hebname(None) is None
    True
    """
    result = None
    if name:
        needle = name.lower()
        result = next((n for n, r in GRAMMAR_NAMES.items() if r.match(needle)), None)
    return result
