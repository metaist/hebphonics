#!/usr/bin/python
# coding: utf-8

"""Hebrew character parsing functions.

This module provides basic functions for classifying Hebrew characters
(or sequences of characters) according to their grammatical function.

NOTE
    This is a "best-effort" parser and while attempts are made at correctness,
    some characters may be underspecified (e.g., specified as "sheva" rather
    than "sheva-na" or "sheva-nah") or incorrectly specified.

PROCESS STEPS
    1. Unicode character names are found for each symbol.
    2. Characters are grouped into (letter + points) groups.
    3. Each character is resolved into a grammatical HebPhonics character.
"""

import re

from . import metadata
from . import codes as U
from . import names as N

globals().update(metadata.metadata())  # add package metadata


def ishataf(name):
    """Return true if the character name is a Hataf- vowel.

    Args:
        name (str): name of character

    Returns:
        bool. True if the character name is a Hataf- vowel; False otherwise.

    Variant spellings are normalized before checking:
    >>> ishataf('HATAF-SEGOL')
    True
    >>> ishataf('hataf-kamats')
    True

    Known characters that are not Hataf- vowels return False:
    >>> ishataf('segol')
    False
    >>> ishataf('alef')
    False

    Unknown character names return False:
    >>> ishataf('hataf-madeup')
    False
    >>> ishataf('invalid-name')
    False
    """
    return N.normalize(name) in [
        N.NAME_HATAF_SEGOL, N.NAME_HATAF_PATAH, N.NAME_HATAF_QAMATS
    ]


def to_names(uni):
    """Return truncated Unicode names for each character in a string.

    Args:
        uni (unicode): a unicode string

    Returns:
        list. Names of the Unicode characters in the string.

    See:
        hebphonics.codes.names()

    Examples:
    >>> to_names(U.LETTER_ALEF + U.LETTER_BET)
    ['LETTER_ALEF', 'LETTER_BET']
    """
    return U.to_names(uni, ignore=True, mode='const')


def to_groups(names):
    """Return a first-order approximation of grouping letters and vowels.

    NOTE:
        This function operates on the names given, not attempt is made to
        verify that the symbols are valid.

    Args:
        names (list): truncated Unicode names for characters

    Returns:
        list. Each list item is itself a list of Unicode letters and vowels.

    Names with an unknown prefix:
    >>> to_groups(['UNKNOWN_TOKEN'])
    []

    >>> to_groups(['LETTER_BET', 'POINT_DAGESH_OR_MAPIQ',
    ...     'POINT_SHEVA', 'SOLIDUS', 'LETTER_RESH', 'POINT_TSERE']) == [
    ...     ['LETTER_BET', 'POINT_DAGESH_OR_MAPIQ', 'POINT_SHEVA'],
    ...     ['SOLIDUS'], ['LETTER_RESH', 'POINT_TSERE']]
    True
    """
    result, group = [], []
    for name in names:
        prefix = None
        regex = re.match('([^_]*)_', name)
        if regex:
            prefix = regex.groups()[0]

        if prefix in ['LETTER'] or name in ['SOLIDUS']:
            if group:  # save any previously constructed group
                result.append(group)
            group = [name]
        elif prefix in ['POINT', 'PUNCTUATION']:
            group.append(name)
        else:  # some unknown token
            prefix = 'UNKNOWN'
            continue

    if group:  # save last group, if any
        result.append(group)

    return result
