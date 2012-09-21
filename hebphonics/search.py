#!/usr/bin/python
# coding: utf-8

"""High-level HebPhonics functions.
"""

from . import metadata, db

globals().update(metadata.metadata())  # add package metadata

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


def _filter_gematria(query, criteria):
    """Return a query filtered by gematria.

    Args:
        query (Query): query to filter
        criteria (int, tuple, list, or dict):
            if an int - the exact value to filter
            if a tuple - the min, max (exclusive)
            if a list - the min, max (inclusive)
            if a dict - a list of operators (__eq__, __lt__, __gt__, __le__,
                __ge__) mapped to values

    Returns:
        Query. the given query filtered by the given filter
    """
    g_filter = {}
    g_type = type(criteria)

    if g_type is int:
        g_filter['__eq__'] = criteria
    elif g_type in [tuple, list]:
        g_len = len(criteria)
        op_min, op_max = '__gt__', '__lt__'

        if g_type is list:
            op_min, op_max = '__ge__', '__le__'
        if g_len > 0:
            g_filter[op_min] = criteria[0]
        if g_len > 1:
            g_filter[op_max] = criteria[1]
    elif g_type is dict:
        g_filter = criteria

    for operator, val in g_filter.items():
        operator = getattr(db.Word.gematria, operator)
        query = query.filter(operator(val))

    return query


def search(session, limit=1000, **kwargs):
    """Return a list of Words that match the search criteria.

    Args:
        session (Session): the database session to query

    Kwargs:
        limit (int): maximum number of results (default: 1000)

        search_books (list).
        search_shemot (bool): if True, only search within names of G-d

        letters_any (list).
        letters_all (list).
        letters_none (list).
        letters_seq (list).

        filter_shemot (bool): if True, exclude names of G-d
        filter_gematria (int): if given, only include words equal to the value
        filter_syllen (list[int]): if given, only include words with these
            syllable lengths
        filter_frequency (list[int]): if given, only include words with these
            frequencies (0=rare, 5=extremely common)

    Returns:
        list<Word>. Words that match the criteria.
    """
    query = session.query(db.Word)

    get = lambda obj, idx: ((idx in obj) and obj[idx]) or None

    # Search
    #search_books = get(kwargs, 'search_books')
    search_shemot = get(kwargs, 'search_shemot')

    if search_shemot:
        query = query.filter(db.Word.hebrew.op('REGEXP')(SHEMOT_REGEX))

    # Letters

    #letters_any = get(kwargs, 'letters_any')
    #letters_all = get(kwargs, 'letters_all')
    #letters_none = get(kwargs, 'letters_none')
    #letters_seq = get(kwargs, 'letters_seq')

    # Filters
    filter_shemot = get(kwargs, 'filter_shemot')
    filter_gematria = get(kwargs, 'filter_gematria')
    filter_syllen = get(kwargs, 'filter_syllen')
    filter_syllen_hatafs = get(kwargs, 'filter_syllen_hatafs')

    if filter_shemot:
        query = query.filter(db.Word.hebrew.op('NOT REGEXP')(SHEMOT_REGEX))

    if filter_gematria:
        query = _filter_gematria(query, filter_gematria)

    if filter_syllen:
        if type(filter_syllen) is int:
            filter_syllen = [filter_syllen]

        query = query.filter(db.Word.syllen.in_(filter_syllen))

    if filter_syllen_hatafs:
        if type(filter_syllen_hatafs) is int:
            filter_syllen_hatafs = [filter_syllen_hatafs]

        query = query.filter(db.Word.syllen_hatafs.in_(filter_syllen_hatafs))

    # Limits
    if limit:
        query = query.limit(limit)

    return query
