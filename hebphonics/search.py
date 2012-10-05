#!/usr/bin/python
# coding: utf-8

"""High-level HebPhonics functions.
"""

from sqlalchemy.sql import and_, or_

from . import metadata, db

globals().update(metadata.metadata())  # add package metadata


def _list(kwargs, attr):
    """Returns the keyword attribute as a list.
    Args:
        attr (str): name of the attribute

    Returns:
        list. The value of the kwarg or an empty list if it is not given.
    """
    result = []
    if attr in kwargs:
        result = kwargs[attr]

        if type(result) is not list:
            result = [result]
    return result


def _has_letters(lst):
    """Returns a list of conditions for querying by letter.

    Args:
        lst (list): list of letters

    Returns:
        list<Condition>. Conditions for searching for letters.
    """
    return [db.Word.syllables.like('%' + letter + '%') for letter in lst]


def search(session, limit=1000, shemot=False, **kwargs):
    """Return a list of Words that match the search criteria.

    Args:
        session (Session): the database session to query

    Kwargs:
        books (list): names of the books to search
        shemot (bool): if True, allow shemot to be displayed (default: False)
        limit (int): maximum number of results (default: 1000)

        Character Filters:
        - find_any (list): at least one of these characters must appear
        - find_all (list): all of these characters must appear
        - find_none (list): none of these character must apepar
        - find_seq (list): all of these characters in this relative order must
            appear in each word

        Integer Filters:
        - gematria (list[int]): only include words equal to these values
        - syllen (list[int]): only include words with these syllable lengths
        - frequency (list[int]): only include words with these frequencies
            (0=rare, 5=extremely common)

    Returns:
        list<Word>. Words that match the criteria.
    """
    query = session.query(db.Word)

    # Search
    if not shemot:
        query = query.filter_by(shemot=False)

    books = _list(kwargs, 'books')
    if books:
        query = query.join(db.Occurrence, db.Book)\
                     .filter(db.Book.name.in_(books))

    # Letters
    find_any = _list(kwargs, 'find_any')
    find_all = _list(kwargs, 'find_all')
    find_none = _list(kwargs, 'find_none')
    find_seq = _list(kwargs, 'find_seq')

    if find_any:
        query = query.filter(or_(*_has_letters(find_any)))

    if find_all:
        query = query.filter(and_(*_has_letters(find_all)))

    if find_none:
        condition = [~db.Word.syllables.like('%' + letter + '%')
                     for letter in find_none]
        query = query.filter(and_(*condition))  # pylint: disable=W0142

    if find_seq:
        condition = '%' + '%'.join(find_seq) + '%'
        query = query.filter(db.Word.syllables.like(condition))

    # Filters
    gematria = _list(kwargs, 'gematria')
    syllen = _list(kwargs, 'syllen')
    syllen_hatafs = _list(kwargs, 'syllen_hatafs')

    if gematria:
        query = query.filter(db.Word.gematria.in_(gematria))

    if syllen:
        query = query.filter(db.Word.syllen.in_(syllen))

    if syllen_hatafs:
        query = query.filter(db.Word.syllen_hatafs.in_(syllen_hatafs))

    # Limits
    if limit:
        query = query.limit(limit)

    return query
