#!/usr/bin/env python
# coding: utf-8
"""Controllers for HebPhonics."""

# lib
from flask import jsonify, render_template, request
from sqlalchemy.sql import and_, or_
from sqlalchemy.sql.expression import func

# pkg
from .. import app, tokens, __version__, __pubdate__
from ..models import Book, Word, Occurrence
from .jsend import JSend

SYMBOLS = list(tokens.GRAMMAR_NAMES)


@app.route("/")
def index():
    """Home page."""
    version = __version__
    if __pubdate__:
        version = f"{version} ({__pubdate__})"

    return render_template(
        "index.html",
        books=[b.name for b in Book.query.order_by(Book.id).all()],
        symbols=SYMBOLS,
        version=version,
    )


@app.route("/words", methods=["GET", "POST"])
def list_word():
    """Search database."""
    args = request.json
    query = search(**args)
    words = [{"h": w.hebrew, "s": w.syllables, "r": w.rules} for w in query.all()]
    sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
    return jsonify(JSend(data=words, query=sql))


def _list(key: str, vals: dict) -> list:
    """Get a key from a dictionary of values and ensure it is a list."""
    result = vals.get(key, [])
    if not isinstance(result, list):
        result = [result]
    return result


def search(limit=1000, shemot=False, **kwargs):
    """Return a list of Words that match the search criteria.

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
        - find_pat (list): all of these characters in this precise order must
            appear in each word

        Integer Filters:
        - gematria (list[int]): only include words equal to these values
        - syllen (list[int]): only include words with these syllable lengths
        - frequency (list[int]): only include words with these frequencies
            (0=rare, 5=extremely common)

    Returns:
        list<Word>. Words that match the criteria.
    """
    # pylint: disable=too-many-locals, too-many-branches
    query = Word.query

    # Search
    if not shemot:
        query = query.filter_by(shemot=False)

    books_all = _list("books_all", kwargs)
    if books_all:
        query = query.join(Occurrence, Book).filter(Book.name.in_(books_all))

    # Symbols
    find_any = _list("find_any", kwargs)
    find_all = _list("find_all", kwargs)
    find_none = _list("find_none", kwargs)
    find_seq = _list("find_seq", kwargs)
    find_pat = _list("find_pat", kwargs)

    if find_any:
        condition = [Word.syllables.like(f"%'{letter}'%") for letter in find_any]
        query = query.filter(or_(*condition))

    if find_all:
        condition = [Word.syllables.like(f"%'{letter}'%") for letter in find_all]
        query = query.filter(and_(*condition))

    if find_none:
        condition = [~Word.syllables.like(f"%'{letter}'%") for letter in find_none]
        query = query.filter(and_(*condition))

    if find_seq:
        quoted = [f"'{x}'" for x in find_seq]
        condition = f"%{'%'.join(quoted)}%"
        query = query.filter(Word.syllables.like(condition))

    if find_pat:
        quoted = [f"'{x}'" for x in find_pat]
        condition = ", ".join(quoted)
        query = query.filter(Word.parsed.like(f"%{condition}%"))

    # Filters
    gematria = _list("gematria", kwargs)
    syllen = _list("syllen", kwargs)
    syllen_hatafs = _list("syllen_hatafs", kwargs)

    if gematria:
        query = query.filter(Word.gematria.in_(gematria))

    if syllen:
        query = query.filter(Word.syllen.in_(syllen))

    if syllen_hatafs:
        query = query.filter(Word.syllen_hatafs.in_(syllen_hatafs))

    # Order
    order = kwargs.get("order", "alpha")
    if order == "random":
        query = query.order_by(func.random())
    else:
        query = query.order_by(Word.hebrew)

    # Limits
    if limit:
        query = query.limit(limit)

    return query
