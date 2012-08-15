#!/usr/bin/python
# coding: utf-8

"""HebPhonics names for Hebrew characters.

These names differ from the standard Unicode name in that they refer to the
grammatical function of the character rather than its presentation form. For
example, Unicode does not distinguish between a Dagesh-Qal or a Dagesh-Hazaq
where as HebPhonics does.
"""

import re

import __init__ as hebphonics

__author__ = "{0.__author__} <{0.__email__}>".format(hebphonics)
__version__ = hebphonics.__version__

# common regular expressions
_R_HATAF = r"c?hataf-"
_R_MALE = r"-malei?"
_R_SOFIT = lambda n: r"(final-)?" + n + r"(-sofit)?"
_R_MAPIQ = r"mapi[kq]-"

_R_SHEVA = r"she?va"
_R_HIRIQ = r"(ch|h)iri[kq]"
_R_TSERE = r"t[sz]erei?"
_R_SEGOL = r"segg?ol"
_R_PATAH = r"patac?h"
_R_QAMATS = r"[kq]amat[sz]"
_R_HOLAM = r"c?hol[ao]m"

# return the constant name for a HebPhonics character name
_const_name = lambda n: n.upper().replace('-', '_')

# return a compiled regular expression and result tuple
_compile_regex = lambda t: (re.compile(r"^" + t[0] + r"$"), t[1])

# regular expressions for normalizing HebPhonics character names
_NAMES = dict(map(_compile_regex, {
    # Non-Hebrew symbols
    r"space": 'space',
    r"solidus": 'solidus',
    r"(zwj|zero-width-joiner)": 'zwj',

    # Dagesh
    r"(dagesh|mapi[kq]|shuri[kq])": 'dagesh',  # an unclassified dagesh
    r"dagesh-([kq]al|lene)": 'dagesh-qal',
    r"dagesh-(c?haza[kq]|forte)": 'dagesh-hazaq',

    # Punctuation
    r"(meteg|silu[kq])": 'meteg',
    r"ma[kq]a(ph|f)": 'maqaf',

    # Sheva
    _R_SHEVA: r"sheva",  # an unclassified sheva
    _R_SHEVA + r"-na": 'sheva-na',
    _R_SHEVA + r"-nac?h": 'sheva-nah',

    # Hiriq
    _R_HIRIQ: 'hiriq',
    _R_HIRIQ + _R_MALE: 'hiriq-male',  # hiriq + yod

    # Tsere
    _R_TSERE: 'tsere',
    _R_TSERE + _R_MALE: 'tsere-male',  # tsere + (alef|he|yod)

    # Segol
    _R_SEGOL: 'segol',
    _R_HATAF + _R_SEGOL: 'hataf-segol',
    _R_SEGOL + _R_MALE: 'segol-male',  # segol + (alef|he|yod)

    # Patah
    _R_PATAH: 'patah',
    _R_HATAF + _R_PATAH: 'hataf-patah',
    r"(furtive-)?" + _R_PATAH + r"(-g[ae]nuv(ah)?)?": 'patah-genuvah',
    _R_PATAH + _R_MALE: 'patah-male',  # patah + (alef|he)

    # Qamats
    _R_QAMATS + r"(-gadol)?": 'qamats',
    _R_HATAF + _R_QAMATS: 'hataf-qamats',
    _R_QAMATS + r"-([kq]atan|c?hatuf)": 'qamats-qatan',
    _R_QAMATS + _R_MALE: 'qamats-male',  # qamats + (alef|he)

    # Holam
    _R_HOLAM + _R_MALE: 'holam-male',  # holom + (alef|he|vav)
    # TODO: Typically, we see holam + vav; check if alef/he work as well.
    _R_HOLAM + r"(-c?haser)?": 'holam-haser',

    # Qubuts / Shuruq
    r"[kq]ubut[sz]": 'qubuts',
    r"shur[eu][kq]": 'shuruq',

    # Letters
    # Final letters are internally called "{x}-sofit" rather than "final-{x}".
    r"ale(f|ph)": 'alef',
    _R_MAPIQ + r"ale(f|ph)": 'mapiq-alef',
    r"bet": 'bet',
    r"vet": 'vet',
    r"gimm?el": 'gimel',
    r"dalet": 'dalet',
    r"hey?": 'he',
    _R_MAPIQ + r"hey?": 'mapiq-he',
    r"vav": 'vav',
    r"zayin": 'zayin',
    r"c?het": 'het',
    r"tet": 'tet',
    r"y[ou]d": 'yod',
    r"kaf": 'kaf',
    _R_SOFIT(r"kaf"): 'kaf-sofit',
    r"[kc]haf": 'khaf',
    _R_SOFIT(r"[kc]haf"): 'khaf-sofit',
    r"lamed": 'lamed',
    r"mem": 'mem',
    _R_SOFIT(r"mem"): 'mem-sofit',
    r"nun": 'nun',
    _R_SOFIT(r"nun"): 'nun-sofit',
    r"same[ck]h": 'samekh',
    r"ayin": 'ayin',
    r"pey?": 'pe',
    _R_SOFIT(r"pey?"): 'pe-sofit',
    r"fey?": 'fe',
    _R_SOFIT(r"fey?"): 'fe-sofit',
    r"t[sz]adi": 'tsadi',
    _R_SOFIT(r"t[sz]adi"): 'tsadi-sofit',
    r"[kq][ou]f": 'qof',
    r"rei?sh": 'resh',
    r"shin": 'shin',
    r"sin": 'sin',
    r"ta[fv]": 'tav',
    r"sa[fv]": 'sav'
}.items()))

# create constants for each of the HebPhonics character names
globals().update(dict((_const_name(n), n) for n in _NAMES.values()))


def normalize(name):
    """Return the normalized HebPhonics name for a Hebrew charachter.

    Args:
        name (str): character name

    Returns:
        str. normalized name

    Normalization is is case-insensitive:
    >>> normalize('shva')
    'sheva'
    >>> normalize('sHeVa')
    'sheva'

    If the name is not known, the result is ``None``:
    >>> normalize('unknown-name') is None
    True

    The normalized name generally follows the Unicode spelling:
    >>> normalize('aleph')
    'alef'
    >>> normalize('alef')
    'alef'
    >>> normalize('yud')
    'yod'
    >>> normalize('kuf')
    'qof'
    >>> normalize('kamatz')
    'qamats'

    Final letters which are named with a "-sofit" suffix rather than a
    "final-" prefix:
    >>> normalize('final-mem')
    'mem-sofit'
    >>> normalize('kaf-sofit')
    'kaf-sofit'

    HebPhonics is also aware of names that refer to grammatical constructs and
    multi-character symbols:
    >>> normalize('dagesh-chazak')
    'dagesh-hazaq'
    >>> normalize('shva-nach')
    'sheva-nah'
    >>> normalize('patach-ganuvah')
    'patah-genuvah'
    >>> normalize('mapiq-hey')
    'mapiq-he'
    """
    result = None
    needle = name.lower()
    for rule, normal in _NAMES.iteritems():
        if rule.match(needle):
            result = normal
            break

    return result
