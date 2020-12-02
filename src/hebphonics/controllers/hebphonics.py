#!/usr/bin/env python
# coding: utf-8
"""Controllers for HebPhonics."""
# native
import os

# lib
from flask import jsonify, render_template, request
from sqlalchemy.sql import and_, or_
from sqlalchemy.sql.expression import desc, false, func

# pkg
from .. import app, tokens as T, rules, __version__, __pubdate__
from ..grammar import ItemList, Cluster, Parser
from ..models import Book, Word, Freq
from .jsend import JSend


@app.route("/")
def index():
    """Home page."""
    version = __version__
    if __pubdate__:
        version = f"{version} ({__pubdate__})"

    return render_template(
        "index.html",
        books=[b.name for b in Book.query.order_by(Book.id).all()],
        symbols=list(T.SYMBOLS),
        rules=rules.RULES,
        version=version,
        GOOGLE_ANALYTICS_ID=os.getenv("GOOGLE_ANALYTICS_ID"),
    )


@app.route("/words", methods=["GET", "POST"])
def list_word():
    """Search database."""
    args = request.json
    query = search(**args)
    words = [{"h": w.hebrew, "f": w.freq, "r": w.ref} for w in query.all()]
    sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
    return jsonify(JSend(data=words, query=sql))


def _block_letter(base, bclasses, btool, full, fclasses, ftool, rules=""):
    if rules:
        rules = f"[{rules}]"

    tool = "\n".join([x for x in [btool, ftool, rules] if x]).strip()
    if tool:
        tool = f' data-tooltip="{tool}"'
    return f"""
<span class="letter">
    <span class="base {' '.join(bclasses)} has-tooltip-left"{tool}>{base}</span>
    <span class="full {' '.join(fclasses)}">{full}</span>
</span>"""


@app.route("/display", methods=["POST"])
def display_word():
    """Typographical hints for words."""
    word = request.json["word"]
    query = Word.query.filter(Word.hebrew == word).first()
    if query:
        syls = ItemList([ItemList([Cluster(**t) for t in s]) for s in query.syls])
    else:
        parser = Parser()
        parsed = parser.parse(word)
        syls = parser.syl(parsed)

    result = ""
    for num, syl in enumerate(syls):
        if num > 0:
            result += _block_letter(" | ", ["syllable"], "", "", ["syllable"], "")

        for sym in syl:
            lett = f"{T.SYMBOLS.get(sym.letter, '')}{T.SYMBOLS.get(sym.dagesh, '')}"
            vow = T.SYMBOLS.get(sym.vowel, "")
            if sym.vowel in [T.NAME_HOLAM_MALE_VAV, T.NAME_SHURUQ]:
                vow = ""

            result += _block_letter(
                lett,
                [f"letter-{sym.letter}", sym.dagesh],
                sym.letter,
                f"{lett}{vow}",
                [f"vowel-{sym.vowel}"],
                sym.vowel,
                ", ".join(sym.rules),
            )

            if sym.vowel in [T.NAME_HOLAM_MALE_VAV, T.NAME_SHURUQ]:
                lett = T.SYMBOLS.get("vav", "")
                vow = T.SYMBOLS.get(sym.vowel, "")
                result += _block_letter(
                    lett,
                    ["letter-vav"],
                    "",
                    vow,
                    [f"vowel-{sym.vowel}"],
                    sym.vowel,
                    ", ".join(sym.rules),
                )

    return jsonify(
        JSend(
            display=f'<div class="hebrew" dir="rtl">{result}</div>',
            syllables=str([x.flat() for x in syls]),
            rules=str(syls.rules.flat()),
        )
    )


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
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    query = Word.query.join(Freq)

    if not shemot:
        query = query.filter(Word.shemot == false())

    # Books
    books_all = _list("books_all", kwargs)
    if books_all:
        query = query.join(Book).filter(Book.name.in_(books_all))

    # Symbols
    find_any = _list("find_any", kwargs)
    find_all = _list("find_all", kwargs)
    find_none = _list("find_none", kwargs)
    find_seq = _list("find_seq", kwargs)
    find_pat = _list("find_pat", kwargs)

    if find_any:
        condition = [Word.parsed.like(f"%'{letter}'%") for letter in find_any]
        query = query.filter(or_(*condition))

    if find_all:
        condition = [Word.parsed.like(f"%'{letter}'%") for letter in find_all]
        query = query.filter(and_(*condition))

    if find_none:
        condition = [~Word.parsed.like(f"%'{letter}'%") for letter in find_none]
        query = query.filter(and_(*condition))

    if find_seq:
        quoted = [f"'{x}'" for x in find_seq]
        condition = f"%{'%'.join(quoted)}%"
        query = query.filter(Word.parsed.like(condition))

    if find_pat:
        quoted = [f"'{x}'" for x in find_pat]
        condition = ", ".join(quoted)
        query = query.filter(Word.parsed.like(f"%{condition}%"))

    # Rules
    rule_any = _list("rule_any", kwargs)
    rule_all = _list("rule_all", kwargs)
    rule_none = _list("rule_none", kwargs)

    if rule_any:
        condition = [Word.rules.like(f"%'{rule}'%") for rule in rule_any]
        query = query.filter(or_(*condition))

    if rule_all:
        condition = [Word.rules.like(f"%'{rule}'%") for rule in rule_all]
        query = query.filter(and_(*condition))

    if rule_none:
        condition = [~Word.rules.like(f"%'{rule}'%") for rule in rule_none]
        query = query.filter(and_(*condition))

    # Filters
    gematria = _list("gematria", kwargs)
    syllen = _list("syllen", kwargs)
    freq = _list("freq", kwargs)

    if gematria:
        query = query.filter(Word.gematria.in_(gematria))

    if syllen:
        query = query.filter(Word.syllen.in_(syllen))

    freq_col = func.sum(Freq.freq).label("freq")
    if freq:
        condition = [freq_col.between(5 ** n, 5 ** (n + 1)) for n in freq]
        query = query.having(or_(*condition))

    # Order
    order = kwargs.get("order", "alpha")
    if order == "random":
        query = query.order_by(func.random())
    elif order == "freq":
        query = query.order_by(desc("freq"))
    else:
        query = query.order_by(Word.hebrew)

    query = query.order_by(Freq.book_id)
    query = query.add_columns(
        # Word.id, Word.hebrew, Word.parsed, Word.rules, freq_col, Freq.ref
        Word.id,
        Word.hebrew,
        freq_col,
        Freq.ref,
    ).group_by(Word.hebrew)

    # Limits
    if limit:
        query = query.limit(limit)

    return query
