#!/usr/bin/python
# coding: utf-8

"""High-level HebPhonics functions.
"""

from . import metadata, db, hebrew

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


def search(session, limit=1000, **kwargs):
    """Return a list of Words that match the search criteria.

    Args:
        session (Session): the database session to query

    Kwargs:
        limit (int): maximum number of results (default: 1000)

        search_books (list).
        search_shemot (bool).
        letters_any (list).
        letters_all (list).
        letters_none (list).
        letters_seq (list).
        filter_shemot (bool).
        #filter_gematria (list).

    Returns:
        list<Word>. Words that match the criteria.
    """
    query = session.query(db.Word)

    get = lambda obj, idx: ((idx in obj) and obj[idx]) or None

    #search_books = get(kwargs, 'search_books')
    search_shemot = get(kwargs, 'search_shemot')

    #letters_any = get(kwargs, 'letters_any')
    #letters_all = get(kwargs, 'letters_all')
    #letters_none = get(kwargs, 'letters_none')
    #letters_seq = get(kwargs, 'letters_seq')

    filter_shemot = get(kwargs, 'filter_shemot')

    if search_shemot:
        query = query.filter(db.Word.hebrew.op('REGEXP')(SHEMOT_REGEX))

    if filter_shemot:
        query = query.filter(db.Word.hebrew.op('NOT REGEXP')(SHEMOT_REGEX))

    if limit:
        query = query.limit(limit)

    return query
