#!/usr/bin/python
# coding: utf-8

"""Filter for names of HaShem (Shemot).

In Judaism, printing shem-haShem (name of G-d) carries additional obligations.
This module helps filter out those names in cases where the results are likely
to be printed.
"""

import re

from . import metadata

globals().update(metadata.metadata())  # add package metadata

# List of compiled regular expressions for the seven names of G-d that require
# care when printing.
SHEMOT_REGEX = [
    re.compile(pattern)
    for pattern in [
        u'א(ֱ)?ל(ו)?ֹה',  # Shem Elokah
        u'א(.)?ד(ו)?ֹנ[ָ|ַ]י$',  # Shem Adnuth
        u'י(ְ)?הו[ָ|ִ]ה',  # Shem HaVayah
        u'([^י]|^)שׁ[ַ|ָ]ד(ּ)?[ָ|ַ]י$',  # Shakai
        u'^אֵל(.)?$',  # Kel
        u'^יָהּ$',  # Kah
        u'^צְבָאוֹת$'  # Tzvakot
    ]
]


def matches(uni):
    """Returns True if the string is a name of HaShem.

    Args:
        uni (unicode): a unicode string

    Returns:
        bool. True if the sequence is a name of HaShem, False otherwise.
    """
    result = False
    for rule in SHEMOT_REGEX:
        if rule.search(uni):
            result = True
            break

    return result
