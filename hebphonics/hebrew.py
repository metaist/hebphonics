#!/usr/bin/python
# coding: utf-8

"""Hebrew character parsing functions.

This module provides basic functions for classifying Hebrew characters
(or sequences of characters) according to their grammatical function.

NOTE
    This is a "best-effort" parser and while attempts are made at correctness,
    some characters may be underspecified (e.g., specified as "sheva" rather
    than "sheva-na" or "sheva-nah") or incorrectly specified (e.g., "qamats"
    rather than "qamats-qatan").
"""

import re

from . import metadata, codes as U, names as N

globals().update(metadata.metadata())  # add package metadata

### BeGeDKeFeT Conversions ###
BEGEDKEFET = {
    U.LETTER_BET: (N.NAME_VET, N.NAME_BET),
    U.LETTER_GIMEL: (N.NAME_GIMEL, N.NAME_GIMEL),
    U.LETTER_DALET: (N.NAME_DALET, N.NAME_DALET),
    U.LETTER_KAF: (N.NAME_KHAF, N.NAME_KAF),
    U.LETTER_FINAL_KAF: (N.NAME_KHAF_SOFIT, N.NAME_KAF_SOFIT),
    U.LETTER_PE: (N.NAME_FE, N.NAME_PE),
    U.LETTER_FINAL_PE: (N.NAME_FE_SOFIT, N.NAME_PE_SOFIT),
    U.LETTER_TAV: (N.NAME_SAV, N.NAME_TAV)
}


### Niqqud Classification ###
DAGESH_POINT = 'dagesh'
SHEVA_POINT = 'sheva'
HATAF_VOWEL = 'hataf'
LONG_VOWEL = 'long'
SHORT_VOWEL = 'short'
MALE_VOWELS = [N.NAME_HIRIQ, N.NAME_TSERE, N.NAME_SEGOL]
POINT_TYPES = {
    N.NAME_DAGESH: DAGESH_POINT,
    N.NAME_DAGESH_HAZAQ: DAGESH_POINT,
    N.NAME_DAGESH_QAL: DAGESH_POINT,

    N.NAME_SHEVA: SHEVA_POINT,
    N.NAME_SHEVA_NA: SHEVA_POINT,
    N.NAME_SHEVA_NAH: SHEVA_POINT,

    N.NAME_HATAF_SEGOL: HATAF_VOWEL,
    N.NAME_HATAF_PATAH: HATAF_VOWEL,
    N.NAME_HATAF_QAMATS: HATAF_VOWEL,

    N.NAME_HIRIQ: SHORT_VOWEL,
    N.NAME_HIRIQ_MALE: LONG_VOWEL,

    N.NAME_TSERE: LONG_VOWEL,
    N.NAME_TSERE_MALE: LONG_VOWEL,

    N.NAME_SEGOL: SHORT_VOWEL,
    N.NAME_SEGOL_MALE: SHORT_VOWEL,

    N.NAME_PATAH: SHORT_VOWEL,
    N.NAME_PATAH_MALE: SHORT_VOWEL,
    N.NAME_PATAH_GENUVAH: SHORT_VOWEL,

    N.NAME_QAMATS: LONG_VOWEL,
    N.NAME_QAMATS_MALE: LONG_VOWEL,
    N.NAME_QAMATS_QATAN: SHORT_VOWEL,

    N.NAME_HOLAM_MALE: LONG_VOWEL,
    N.NAME_HOLAM_HASER: LONG_VOWEL,

    N.NAME_QUBUTS: SHORT_VOWEL,
    N.NAME_SHURUQ: LONG_VOWEL
}


### Gematria Values ###
GEMATRIA_VALUES = {
    U.LETTER_ALEF: 1,
    U.LETTER_BET: 2,
    U.LETTER_GIMEL: 3,
    U.LETTER_DALET: 4,
    U.LETTER_HE: 5,
    U.LETTER_VAV: 6,
    U.LETTER_ZAYIN: 7,
    U.LETTER_HET: 8,
    U.LETTER_TET: 9,
    U.LETTER_YOD: 10,
    U.LETTER_KAF: 20,
    U.LETTER_FINAL_KAF: 20,
    U.LETTER_LAMED: 30,
    U.LETTER_MEM: 40,
    U.LETTER_FINAL_MEM: 40,
    U.LETTER_NUN: 50,
    U.LETTER_FINAL_NUN: 50,
    U.LETTER_SAMEKH: 60,
    U.LETTER_AYIN: 70,
    U.LETTER_PE: 80,
    U.LETTER_FINAL_PE: 80,
    U.LETTER_TSADI: 90,
    U.LETTER_FINAL_TSADI: 90,
    U.LETTER_QOF: 100,
    U.LETTER_RESH: 200,
    U.LETTER_SHIN: 300,
    U.LETTER_TAV: 400
}

# In Judaism, printing shem-haShem (name of G-d) carries additional
# obligations. This regex matches the seven special names of G-d.
SHEMOT_REGEX = u'(' + u')|('.join([
    u'א(ֱ)?ל(ו)?ֹה',  # Shem Elokah
    u'א(.)?ד(ו)?ֹנ[ָ|ַ]י$',  # Shem Adnuth
    u'י(ְ)?הו[ָ|ִ]ה',  # Shem HaVayah
    u'([^י]|^)שׁ[ַ|ָ]ד(ּ)?[ָ|ַ]י$',  # Shakai
    u'^אֵל(.)?$',  # Kel
    u'^יָהּ$',  # Kah
    u'^צְבָאוֹת$'  # Tzvakot
]) + u')'


def pointtype(point):
    """Return the type of point or None.

    Args:
        point (str): the point name (per hebphonics.names)

    Returns:
        str or None. The type of point ('hataf', 'short', 'long', 'sheva', or
        'dagesh') or None if the name is not a name of a point.

    Examples:
    >>> pointtype('hataf-segol') == HATAF_VOWEL
    True
    >>> pointtype('qubuts') == SHORT_VOWEL
    True
    >>> pointtype('sheva-nah') == SHEVA_POINT
    True
    >>> pointtype('dagesh-hazaq') == DAGESH_POINT
    True
    >>> pointtype('alef') is None
    True
    >>> pointtype(None) is None
    True
    >>> pointtype(['alef']) is None
    True
    >>> pointtype(['dagesh-qal']) == DAGESH_POINT
    True
    """
    result = None
    if not point:
        return result
    elif type(point) is list:
        point = point[0]

    name = N.normalize(point)

    try:
        result = POINT_TYPES[name]
    except KeyError:
        result = None

    return result


def isvowel(point):
    """Return True if the point name is a vowel.

    >>> isvowel(N.NAME_QAMATS)
    True
    """
    return pointtype(point) in [HATAF_VOWEL, SHORT_VOWEL, LONG_VOWEL]


def gematria(uni):
    """Return the numerical value of a Hebrew string.

    Args:
        uni (unicode): unicode string

    Returns:
        int. numerical value of the string
    """
    return sum([
        GEMATRIA_VALUES[letter]
        for letter in uni
        if letter in GEMATRIA_VALUES
    ])


def isshemot(uni):
    """Returns True if the given unicode string contains a name of G-d.

    Args:
        uni (unicode): word to check

    Returns:
        bool. True if the word is a name of G-d.
    """
    return re.search(SHEMOT_REGEX, uni, re.I + re.U) is not None


class Cluster(object):
    """Hebrew symbol cluster; a letter, dagesh, vowel, and points."""
    letter, dagesh, vowel, points = None, None, None, None

    def __init__(self, letter=None, dagesh=None, vowel=None, points=None):
        """Construct a Cluster.

        Args:
            letter (str): name of the letter
            dagesh (str): type of dagesh (dagesh, dagesh-hazaq/-qal, mapiq)
            vowel (str): name of the vowel
            points (list): list of points

        >>> Cluster() is not None
        True
        """
        self.set(letter=letter, dagesh=dagesh, vowel=vowel, points=points)
        if points is None:
            self.points = []

    def __nonzero__(self):
        """Returns (bool) True if a Cluster is non-empty.

        >>> (Cluster() or False)
        False
        """
        return len(self.tolist()) > 0

    def __repr__(self):
        """Returns (str) a stricter representation.

        >>> repr(Cluster())
        'Cluster(letter=None, dagesh=None, vowel=None, points=[])'
        """
        return ('Cluster(letter={0.letter!r}, dagesh={0.dagesh!r}, '
                'vowel={0.vowel!r}, points={0.points!r})').format(self)

    def __str__(self):
        """Returns (str) a string representation.

        >>> str(Cluster())
        '[]'
        """
        return str(self.tolist())

    def tolist(self):
        """Returns (list) a list representation of the cluster.

        >>> Cluster().tolist()
        []
        """
        return [item for item in [self.letter, self.dagesh, self.vowel]
                if item] + self.points

    def addpoint(self, point):
        """Adds a point to this cluster.

        >>> x = Cluster()
        >>> x.addpoint('Y').tolist()
        ['Y']
        """
        self.points.append(point)
        return self

    def set(self, letter=None, dagesh=None, vowel=None, points=None):
        """Sets the attributes of the cluster.

        >>> Cluster(letter='W', dagesh='X', vowel='Y', points=['Z']).tolist()
        ['W', 'X', 'Y', 'Z']
        """
        if letter:
            self.letter = letter

        if dagesh:
            self.dagesh = dagesh

        if vowel:
            self.vowel = vowel

        if points:
            self.points = points

        return self


def _parse_letter(cluster, prev, result):
    """Returns the cluster resulting from parsing a letter.

    Args:
        cluster (Cluster): the current cluster of unparsed tokens
        prev (Cluster): the previously parsed cluster; may be modified
        result (Cluster): the current cluster of semi-parsed tokens

    Returns:
        (Cluster, Cluster). The previous cluster (with any modifications) and
        the currently parsed cluster.
    """
    isfirst = not prev

    if cluster.letter in [U.LETTER_ALEF, U.LETTER_HE] and cluster.dagesh:
        # {X}: an alef / he followed by a dagesh is a mapiq-
        result.set(
            dagesh=N.NAME_MAPIQ,
            letter=N.NAME_MAPIQ + '-' + result.letter
        )
    elif cluster.letter in BEGEDKEFET:
        letter_name, changed_name = BEGEDKEFET[cluster.letter]
        result.letter = letter_name
        if cluster.dagesh:
            # {X}: dagesh in begedkefet is qal unless preceded by vowel
            dagesh = N.NAME_DAGESH_QAL
            if prev and isvowel(prev.vowel):
                dagesh = N.NAME_DAGESH_HAZAQ

            # {X}: begedkefet followed by dagesh changes sound/name
            result.set(letter=changed_name, dagesh=dagesh)
    elif U.LETTER_VAV == cluster.letter and cluster.dagesh:
        # {X}: vav-dagesh is shuruq if not preceded by a vowel
        if isfirst or not isvowel(prev.vowel):
            # this is really a vowel
            result = Cluster()  # reset cluster
            (prev or result).vowel = N.NAME_SHURUQ
    elif U.LETTER_YOD == cluster.letter:
        if (not cluster.points and  # no points on this yod
            not cluster.dagesh and  # no dagesh on this yod
                (prev and prev.vowel in MALE_VOWELS)):
            # {X}: a hiriq / tsere / segol followed by a yod is a -male
            prev.vowel += '-male'
    elif U.LETTER_SHIN == cluster.letter:
        letter_name = N.NAME_SIN  # default case for Yissacher
        if U.POINT_SHIN_DOT in cluster.points:
            letter_name = N.NAME_SHIN
        elif U.POINT_SIN_DOT in cluster.points:
            letter_name = N.NAME_SIN
        result.letter = letter_name

    return prev, result


def _parse_vowel(point, prev, result, islast=False):
    """Returns the cluster resulting from parsing a vowel.

    Args:
        point (uni): normalized unicode point being parsed
        prev (Cluster): the previously parsed cluster; may be modified
        result (Cluster): the current cluster of semi-parsed tokens

    Kwargs:
        islast (bool): whether this is the last cluster (default: False)

    Returns:
        (Cluster, Cluster). The previous cluster (with any modifications) and
        the currently parsed cluster.
    """
    isfirst = not prev

    if U.POINT_PATAH == point and islast:
        result.vowel += '-genuvah'
    elif U.POINT_HOLAM_HASER_FOR_VAV == point:
        result.vowel = N.NAME_HOLAM_HASER
    elif U.POINT_HOLAM == point:
        result.vowel = N.NAME_HOLAM_HASER
        if N.NAME_VAV == result.letter and not result.dagesh:
            # this is really a vowel
            result = Cluster()  # reset result
            (prev or result).vowel = N.NAME_HOLAM_MALE
    elif U.POINT_HATAF_QAMATS == point:
        if prev and N.NAME_QAMATS == prev.vowel:
            # {X}: qamats before a hataf-qamats is -qatan
            # make this parse rule optional
            prev.vowel = N.NAME_QAMATS_QATAN
    elif U.POINT_SHEVA == point:
        if islast:
            # {X}: last syllable -> sheva-nah
            result.vowel = N.NAME_SHEVA_NAH
        elif (
            # {X}: start of word or syllable -> sheva-na
            isfirst or

            # {X}: under dagesh-hazaq -> sheva-na
            N.NAME_DAGESH_HAZAQ == result.dagesh or

            # {X}: after long vowel -> sheva-na
            LONG_VOWEL == pointtype(prev.vowel)
        ):
            result.vowel = N.NAME_SHEVA_NA
        elif (prev.vowel and prev.vowel.startswith(N.NAME_SHEVA)):
            # {X}: two in a row -> sheva-nah, sheva-na
            prev.vowel = N.NAME_SHEVA_NAH
            result.vowel = N.NAME_SHEVA_NA

    return prev, result


def _parse(tokens, prev, cluster, islast=False):
    """Returns a parsed cluster of tokens.

    Args:
        tokens (uni): normalized unicode string being parsed
        prev (Cluster): the previously parsed cluster; may be modified
        cluster (Cluster): the current cluster of unparsed tokens

    Kwargs:
        islast (bool): whether this is the last cluster (default: False)

    Returns:
        (Cluster, Cluster). The previous cluster (with any modifications) and
        the currently parsed cluster.
    """
    letter_name = U.name(cluster.letter).lower()
    if letter_name.startswith('final_'):
        letter_name = letter_name[6:] + '-sofit'

    vowel_name = None
    if cluster.points:  # guess the name of the vowel
        vowel_name = U.name(cluster.points[0]).lower().replace('_', '-')
        if not pointtype(vowel_name):
            vowel_name = None

    result = Cluster(
        letter=letter_name,
        dagesh=cluster.dagesh,
        vowel=vowel_name
    )  # best guess

    prev, result = _parse_letter(cluster, prev, result)
    # letter parsed

    if N.NAME_DAGESH == result.dagesh:
        # {X}: an unclassified dagesh is always a dagesh-hazaq
        result.dagesh = N.NAME_DAGESH_HAZAQ

    for point in cluster.points:
        if U.POINT_QAMATS == point and U.PUNCTUATION_MAQAF in tokens:
            # {X}: qamats in non-last word connected by maqafs is -qatan
            result.vowel = N.NAME_QAMATS_QATAN
        else:
            prev, result = _parse_vowel(point, prev, result, islast=islast)
    # niqqud parsed

    return prev, result


def clusters(uni):
    """Returns a list of parsed clusters in a Hebrew string.

    Args:
        uni (unicode): unicode string

    Returns:
        list<Cluster>. Clusters of parsed symbols.
    """
    result, cluster = [], Cluster()
    tokens = U.normalize(uni)

    def add_results(cluster, islast=False):
        """Parse and add results."""
        prev = (result and result[-1]) or Cluster()

        if cluster:
            prev, cluster = _parse(tokens, prev, cluster, islast)
            if prev:  # previous was modified
                result[-1] = prev

            if cluster:  # current cluster parsed
                result.append(cluster)

    for token in tokens:
        token_name = U.name(token, mode='const')

        if token_name.startswith('LETTER_'):
            add_results(cluster)
            cluster = Cluster(letter=token)
        elif U.POINT_DAGESH_OR_MAPIQ == token:
            cluster.dagesh = N.NAME_DAGESH
        elif token_name.startswith('POINT_'):
            cluster.addpoint(token)

    add_results(cluster, islast=True)

    return result


def parse(uni):
    """Return the names of the letters and niqqud in a string.

    Args:
        uni (unicode): a Hebrew Unicode string

    Returns:
        list. Names of the parse character names.
    """
    return [item for group in clusters(uni)
            for item in group.tolist()]


def syllabify(uni=None, groups=None, strict=False):
    """Returns a list of syllables.

    Either a unicode string (uni) or a list of clusters (groups) must be
    provided.

    Kwargs:
        uni (unicode): unicode string (default: None)
        groups (list<Cluster>): list of cluster (default: None)
        strict (bool): if True, follow rules of havarot (default: False)

    Returns:
        list<list<str>>. List of syllables (a lists of strings).
    """
    assert (uni or clusters), 'must provide a unicode string or clusters'
    result, syllable = [], []
    groups = groups or clusters(uni)
    syllable_break, last_vowel = False, ''

    for group in groups:
        curr_type = pointtype(group.vowel)
        last_type = pointtype(last_vowel)
        syllable_break = (
            # {X}: syllable break BEFORE a any vowel
            isvowel(group.vowel) or

            # {X}: (lax) syllable break BEFORE hataf-vowel
            (not strict and HATAF_VOWEL == curr_type) or

            # {X}: syllable break AFTER sheva-nah
            N.NAME_SHEVA_NAH == last_vowel
        ) and not (
            # {X}: no syllable break AFTER a sheva-na
            N.NAME_SHEVA_NA == last_vowel or

            # {X}: (strict) no syllable break AFTER hataf-vowel
            (strict and HATAF_VOWEL == last_type)
        )

        if syllable and syllable_break:
            result.append(syllable)
            syllable = []

        syllable += group.tolist()
        last_vowel = (group.vowel or '')

    # iterated through all groups

    if syllable:  # add the last syllable
        result.append(syllable)

    return result
