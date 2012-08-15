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

import metadata
import codes
import names

U, N = codes, names  # alias
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
    check = names.normalize(name)
    return check in [N.HATAF_SEGOL, N.HATAF_PATAH, N.HATAF_QAMATS]
