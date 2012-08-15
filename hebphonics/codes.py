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

import metadata

globals().update(metadata.metadata())  # add package metadata

# filter function to retain only valid Unicode characters
_is_unicode = lambda u: '' != unicodedata.name(u, '')

# return the Unicode name for a Unicode character
_unicode_name = lambda u: (
    unicodedata.name(u, 'U+' + hex(ord(u)).replace('x', ''))
)

# return the HebPhonics name ("HEBREW " prefix and punctuation removed
_const_name = lambda u: (
    re.sub('[ -]', '_', _unicode_name(u).replace('HEBREW ', ''))
)

# return the HebPhonics short name (same as above, with further prefix removed)
_short_name = lambda u: (
    re.sub(
        '^(ACCENT|LETTER|LIGATURE|MARK|POINT|PUNCTUATION)_', '',
        _const_name(u)
    )
)

# Unicode code points
_POINTS = filter(_is_unicode, map(unichr, [
    # C0 Controls and Basic Latin
    # <http://www.unicode.org/charts/PDF/U0000.pdf>
    int('0020', 16),  # SPACE
    int('002F', 16),  # SOLIDUS; used as morphological divider in Tanach

    # General Punctuation
    # <http://www.unicode.org/charts/PDF/U2000.pdf>
    int('200D', 16)] +  # ZERO WIDTH JOINER

    # Hebrew
    # <http://www.unicode.org/charts/PDF/U0590.pdf>
    range(int('0590', 16), int('05F4', 16)) +

    # Alphabet Presentation Forms
    # <http://www.unicode.org/charts/PDF/UFB00.pdf>
    range(int('FB1D', 16), int('FB4F', 16))
))

globals().update(dict((_const_name(char), char) for char in _POINTS))


def names(uni, ignore=False, type='const'):
    """Return a list of Unicode names for each character in string.

    Args:
        uni (unicode): unicode string

    Kwargs:
        ignore (bool): whether or not to exclude code points outside of
            HebPhonics (default: False)
        type (str): one of:
            * 'unicode': return the full Unicode character name
            * 'const': (default) return the HebPhonics constant name
            * 'short': same as 'const', but with another prefix removed

    Returns:
        list. String names of each Unicode code point in the given string.

    Examples:
    >>> names(LETTER_ALEF + POINT_HIRIQ)
    ['LETTER_ALEF', 'POINT_HIRIQ']
    >>> names(LETTER_ALEF + POINT_HIRIQ, type='short')
    ['ALEF', 'HIRIQ']

    Invalid type raises an AssertionError:
    >>> try: names(LETTER_ALEF, type='foo')
    ... except AssertionError, e: print e
    type must be one of ['unicode', 'const', 'short']

    Characters outside of HebPhonics can be omitted:
    >>> names(LETTER_ALEF + u'\u00C1')
    ['LETTER_ALEF', 'LATIN_CAPITAL_LETTER_A_WITH_ACUTE']
    >>> names(LETTER_ALEF + u'\u00C1', ignore=True)
    ['LETTER_ALEF']
    """
    assert type in ['unicode', 'const', 'short'], (
        "type must be one of ['unicode', 'const', 'short']"
    )

    f = {
        'unicode': _unicode_name,
        'const': _const_name,
        'short': _short_name
    }[type]

    return [
        f(char) for char in uni
        if not ignore or char in _POINTS
    ]
