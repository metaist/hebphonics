#!/usr/bin/python
# coding: utf-8

"""High-level HebPhonics functions.
"""

from sqlalchemy.sql import and_, or_

from . import metadata, db

globals().update(metadata.metadata())  # add package metadata


def _list(obj):
    """Returns a list version of the given object.

    Args:
        obj (any): the item to listify

    Returns:
        list. The object or a list with the object as a single item.

    >>> _list(None)
    []
    >>> _list(1)
    [1]
    >>> _list([1])
    [1]
    >>> _list('1')
    ['1']
    """
    result = obj
    if obj is None:
        result = []
    elif type(obj) is not list:
        result = [obj]
    return result


def _get(obj, idx):
    """Returns the item at the given index if it exists or None.

    Args:
        obj (dict): item to access
        idx (str): key to access

    Returns:
        any. The value of the item at the given key or None if the key is not
        in the dict.

    >>> _get({}, 'foo') is None
    True
    >>> _get({'a': 1}, 'a')
    1
    """
    return ((idx in obj) and obj[idx]) or None


def _letters(query, **kwargs):
    """Returns the query after letters have been filtered.

    Args:
        query (Query): query to filter

    Kwargs:
        (multiple): lists of letter criteria

    Returns:
        Query. The given query with letter criteria applied.
    """
    # Letters
    has_letters = lambda lst: [db.Word.syllables.like('%' + letter + '%')
                               for letter in lst]
    letters_any = _list(_get(kwargs, 'letters_any'))
    letters_all = _list(_get(kwargs, 'letters_all'))
    letters_none = _list(_get(kwargs, 'letters_none'))
    letters_seq = _list(_get(kwargs, 'letters_seq'))

    if letters_any:
        query = query.filter(or_(*has_letters(letters_any)))

    if letters_all:
        query = query.filter(and_(*has_letters(letters_all)))

    if letters_none:
        condition = [~db.Word.syllables.like('%' + letter + '%')
                     for letter in letters_none]
        query = query.filter(and_(*condition))  # pylint: disable=W0142

    if letters_seq:
        condition = '%' + '%'.join(letters_seq) + '%'
        query = query.filter(db.Word.syllables.like(condition))

    return query


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


def _filters(query, **kwargs):
    """Returns the query after filter criteria have been applied.

    Args:
        query (Query): the query to filter

    Kwargs:
        (multiple): the filters to apply

    Returns:
        Query. The given query with additional filters applied.
    """
    # Filters
    filter_shemot = _get(kwargs, 'filter_shemot')
    filter_gematria = _get(kwargs, 'filter_gematria')
    filter_syllen = _list(_get(kwargs, 'filter_syllen'))
    filter_syllen_hatafs = _list(_get(kwargs, 'filter_syllen_hatafs'))

    if filter_shemot:
        query = query.filter_by(shemot=False)

    if filter_gematria:
        query = _filter_gematria(query, filter_gematria)

    if filter_syllen:
        query = query.filter(db.Word.syllen.in_(filter_syllen))

    if filter_syllen_hatafs:
        query = query.filter(db.Word.syllen_hatafs.in_(filter_syllen_hatafs))

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

    # Search
    search_books = _list(_get(kwargs, 'search_books'))
    search_shemot = _get(kwargs, 'search_shemot')

    if search_books:
        query = query.join(db.Occurrence, db.Book)\
                     .filter(db.Book.name.in_(search_books))

    if search_shemot:
        query = query.filter_by(shemot=True)

    query = _letters(query, **kwargs)
    query = _filters(query, **kwargs)

    # Limits
    if limit:
        query = query.limit(limit)

    return query
