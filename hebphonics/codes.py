#!/usr/bin/python
# coding: utf-8

"""Unicode characters and code points used in HebPhonics.

This module defines constants representing the Unicode characters for Hebrew
(and Yiddish). Utility functions are provided to convert unicode strings
into a list of unicode code point names and vice-versa.

NAMING
    The constants are named following the Unicode 6.1 standard with punctuation
    (spaces, dashes) replaced by underscores and the prefix "HEBREW " removed.

CODE POINTS
    * `Hebrew <//www.unicode.org/charts/PDF/U0590.pdf>`_
    * `Alphabetic Presentation Forms <//www.unicode.org/charts/PDF/UFB00.pdf>`_
    * Miscellaneous (SPACE, SOLIDUS, ZERO WIDTH JOINER)
"""

import re
import unicodedata

from . import metadata

globals().update(metadata.metadata())  # add package metadata

# filter function to retain only valid Unicode characters
_IS_UNICODE = lambda u: '' != unicodedata.name(u, '')

# return the Unicode name for a Unicode character
_UNICODE_NAME = lambda u: (
    unicodedata.name(u, 'U+' + hex(ord(u)).replace('x', ''))
)

# return the HebPhonics name ("HEBREW " prefix and punctuation removed
_CONST_NAME = lambda u: (
    re.sub('[ -]', '_', _UNICODE_NAME(u).replace('HEBREW ', ''))
)

# return the HebPhonics short name (same as above, with further prefix removed)
_SHORT_NAME = lambda u: (
    re.sub(
        '^(ACCENT|LETTER|LIGATURE|MARK|POINT|PUNCTUATION)_', '',
        _CONST_NAME(u)
    )
)

# Unicode code points
_RANGES = ([
    # C0 Controls and Basic Latin
    # <http://www.unicode.org/charts/PDF/U0000.pdf>
    int('0020', 16),  # SPACE
    int('002F', 16),  # SOLIDUS; used as morphological divider in Tanach

    # General Punctuation
    # <http://www.unicode.org/charts/PDF/U2000.pdf>
    int('200D', 16)  # ZERO WIDTH JOINER
] +
    # Hebrew
    # <http://www.unicode.org/charts/PDF/U0590.pdf>
    range(int('0590', 16), int('05F4', 16)) +

    # Alphabet Presentation Forms
    # <http://www.unicode.org/charts/PDF/UFB00.pdf>
    range(int('FB1D', 16), int('FB4F', 16))
)

_POINTS = [
    unichr(_num)
    for _num in _RANGES
    if _IS_UNICODE(unichr(_num))
]

globals().update(dict((_CONST_NAME(char), char) for char in _POINTS))


def normalize(uni):
    """Returns a normalized decomposed unicode string.

    Args:
        uni (unicode): unicode string

    Returns:
        unicode. A normalized and decomposed Unicode string.
    """
    return unicodedata.normalize('NFKD', uni)


def strip(uni):
    """Returns the unicode strign with only letters and points.

    Note:
        Normalization is performed on each character rather than on the entire
        string.

    Args:
        uni (unicode): unicode string

    Returns:
        unicode. A normalized string with only letters and points.

    Examples:
    >>> strip(LETTER_ALEF) == LETTER_ALEF
    True
    >>> strip(LETTER_ALEF + POINT_PATAH) == LETTER_ALEF + POINT_PATAH
    True
    >>> strip(LETTER_ALEF+POINT_PATAH + PUNCTUATION_MAQAF) == (LETTER_ALEF +
    ...     POINT_PATAH)
    True
    """
    result = ''
    for char in uni:
        char_name = name(char, mode='const')
        if (char_name.startswith('LETTER_') or
                char_name.startswith('POINT_')):
            result += normalize(char)

    return result


def name(char, ignore=True, mode='short'):
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
    >>> name(LETTER_ALEF, mode='const')
    'LETTER_ALEF'
    >>> [name(x, mode='const') for x in LETTER_ALEF + POINT_HIRIQ]
    ['LETTER_ALEF', 'POINT_HIRIQ']
    >>> [name(x, mode='short') for x in LETTER_ALEF + POINT_HIRIQ]
    ['ALEF', 'HIRIQ']

    Invalid mode raises an AssertionError:
    >>> try: name(LETTER_ALEF, mode='foo')
    ... except AssertionError, e: print e
    mode must be one of ['unicode', 'const', 'short']

    Characters outside of HebPhonics can be allowed:
    >>> [name(x, mode='const') for x in LETTER_ALEF + u'\u00C1' if name(x)]
    ['LETTER_ALEF']
    >>> [name(x, ignore=False, mode='const') for x in LETTER_ALEF + u'\u00C1']
    ['LETTER_ALEF', 'LATIN_CAPITAL_LETTER_A_WITH_ACUTE']

    >>> name('') is None
    True
    """
    assert mode in ['unicode', 'const', 'short'], (
        "mode must be one of ['unicode', 'const', 'short']"
    )

    result = None
    if not char:
        return result

    func = {
        'unicode': _UNICODE_NAME,
        'const': _CONST_NAME,
        'short': _SHORT_NAME
    }[mode]

    if char in _POINTS or not ignore:
        result = func(char)

    return result
