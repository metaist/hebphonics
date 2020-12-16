#!/usr/bin/env python
# coding: utf-8
"""Controllers for HebPhonics."""

# native
import os
from inspect import cleandoc

# lib
from flask import jsonify, render_template, request
from sqlalchemy.sql import and_, or_
from sqlalchemy.sql.expression import desc, false, func
from markdown import markdown

# pkg
from .. import app, tokens as T, rules, __version__, __pubdate__
from ..grammar import ItemList, Cluster, Parser
from ..models import Book, Word, Freq
from .jsend import JSend


VERSION = __version__ if not __pubdate__ else f"{__version__} ({__pubdate__})"
GOOGLE_ANALYTICS_ID = os.getenv("GOOGLE_ANALYTICS_ID")


def get_color(count):
    """Simple color scale."""
    color = ""
    if count == 0:
        color = "is-danger"
    elif count < 20:
        color = "is-warning"
    elif count < 300:
        color = "is-primary"
    elif count < 1000:
        color = "is-success"
    else:
        color = "is-black"
    return color


@app.route("/")
def index():
    """Home page."""
    return render_template(
        "index.html",
        books=[b.name for b in Book.query.order_by(Book.id).all()],
        symbols=list(T.SYMBOLS),
        rules=rules.RULES,
        version=VERSION,
        GOOGLE_ANALYTICS_ID=GOOGLE_ANALYTICS_ID,
    )


@app.route("/rules")
def list_rules():
    """Get rules list from the database."""
    all_rules = {}
    all_symbols = {}
    see_also = rules.__doc__[rules.__doc__.find("See also:") + 10 :]
    for rule, fn in rules.RULES.items():
        count = (
            Word.query.filter(Word.rules.like(f"%'{rule}'%"))
            .with_entities(func.count())
            .scalar()
        )

        parts = cleandoc(fn.__doc__ or "").split("\n")
        stmt = f"- **Rule**: {parts[0]}"
        rest = (
            "\n".join(parts[1:])
            .replace("Example:", "- **Example**:")
            .replace("Examples:", "- **Examples**:")
            .replace("Requires:", "- **Requires**:")
            .replace("See also:", "- **See also**:")
            .replace("Source:", "- **Source**:")
            .replace("Sources:", "- **Sources**:")
        )

        doc = markdown(f"{rest}\n\n{stmt}\n\n{see_also}")
        all_rules[rule] = dict(doc=doc, count=f"{count:,}", color=get_color(count))

    for symbol in T.SYMBOLS:
        count = (
            Word.query.filter(Word.parsed.like(f"%'{symbol}'%"))
            .with_entities(func.count())
            .scalar()
        )
        all_symbols[symbol] = dict(count=f"{count:,}", color=get_color(count))

    return render_template(
        "rules.html",
        rules=all_rules,
        symbols=all_symbols,
        version=VERSION,
        GOOGLE_ANALYTICS_ID=GOOGLE_ANALYTICS_ID,
    )


@app.route("/words", methods=["GET", "POST"])
def list_word():
    """Search database."""
    args = request.json
    query = search(**args)
    words = [{"h": w.hebrew, "f": w.freq, "r": w.ref} for w in query.all()]
    sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
    return jsonify(JSend(data=words, query=sql))


def _block_letter(base, bclasses, btool, full, fclasses, ftool, dtool, rules_=""):
    if rules_:
        rules_ = f"[{rules_}]"

    tool = "\n".join([x for x in [btool, dtool, ftool, rules_] if x]).strip()
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
            result += _block_letter(" | ", ["syllable"], "", "", ["syllable"], "", "")

        for sym in syl:
            lett = f"{T.SYMBOLS.get(sym.letter, '')}{T.SYMBOLS.get(sym.dagesh, '')}"
            vow = T.SYMBOLS.get(sym.vowel, "")
            if sym.vowel in [T.NAME_HOLAM_MALE_VAV, T.NAME_SHURUQ]:
                vow = ""

            lett_show = [T.POINT_HOLAM, T.LETTER_FINAL_KAF]
            lett_hide = [T.LETTER_AYIN]

            result += _block_letter(
                lett,
                [f"letter-{sym.letter}", sym.dagesh],
                sym.letter,
                f"{lett if (lett in lett_show or vow in lett_show) and not (lett in lett_hide or vow in lett_hide) else ' '}{vow}",
                [f"vowel-{sym.vowel}"],
                sym.vowel,
                sym.dagesh,
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
                    sym.dagesh,
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
        query = query.order_by(desc("freq"), Freq.book_id, Word.id)
    elif order == "alpha":
        query = query.order_by(Word.hebrew, Freq.book_id, Word.id)
    elif order == "source":
        query = query.order_by(Freq.book_id, Word.id)

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
