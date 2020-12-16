#!/usr/bin/env python
# coding: utf-8
"""Parsers for Hebrew texts."""

__all__ = ["chabad_org", "tanach_us", "mechon_mamre_org"]

# native
from dataclasses import dataclass
from functools import partial
from inspect import cleandoc
from multiprocessing import Process, RLock, Queue
from pathlib import Path
from typing import Any, List, Optional
from zipfile import ZipFile
import io
import os
import queue
import re
import shutil

# lib
from docopt import docopt
from sqlalchemy import func
from tqdm import tqdm
import requests

# pkg
from .. import app, grammar, tokens as T
from ..models import db_create, db, Book, Word, Freq

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
)


@dataclass
class Msg:
    """Message for a queue."""

    kind: str = ""
    data: Any = None


def queuer(q: Queue) -> Msg:
    """Yield messages from a queue."""
    while True:
        try:
            msg = q.get(block=True, timeout=0.05)
            if msg.kind == "END":
                break
            yield msg
        except queue.Empty:
            continue


def notify_and_join(q: Queue, procs: List[Process]):
    """Notify a list of processes to end and wait for them to join."""
    for _ in range(len(procs)):
        q.put(Msg(kind="END"))
    # all processes notified

    for p in procs:
        p.join()
    # all processes ended


def parse_args(doc: str, argv: Optional[List[str]] = None):
    """Parse common args."""
    args = docopt(cleandoc(doc or ""), argv=argv)
    num_cpus = os.cpu_count() if args["--cpus"] == "all" else int(args["--cpus"])
    num_writers = 1
    num_readers = max(num_cpus - num_writers, 1)
    args.update(num_writers=num_writers, num_readers=num_readers)
    return args


def download_unzip(url: str, dest: Path, pattern: re.Pattern = None) -> Path:
    """Download a zip file; extracting only files that match `pattern`."""
    print(f"downloading {url}")
    res = requests.get(url, headers={"User-Agent": USER_AGENT})
    with ZipFile(io.BytesIO(res.content)) as file:
        sources = (
            file.namelist()
            if not pattern
            else [p for p in file.namelist() if pattern.match(p)]
        )

        dest.mkdir(parents=True, exist_ok=True)
        for item in tqdm(sources):
            name = Path(item).name
            with file.open(item) as source, (dest / name).open("wb") as target:
                shutil.copyfileobj(source, target)
            # print(f"extracted {name}")
    return dest


def spawn_processes(init_fn, read_fn, write_fn, num_readers=1, num_writers=1):
    """Start readers and writers."""
    tqdm.set_lock(RLock())

    write_q = Queue()
    write_fn = partial(write_fn, lock=tqdm.get_lock(), write_q=write_q)
    writers = [
        Process(daemon=True, target=partial(write_fn, pos=i))
        for i in range(num_writers, 0, -1)
    ]

    read_q = Queue()
    read_fn = partial(read_fn, lock=tqdm.get_lock(), read_q=read_q, write_q=write_q)
    readers = [
        Process(daemon=True, target=partial(read_fn, pos=i))
        for i in range(num_readers + 1, num_writers, -1)
    ]

    for p in readers + writers:
        p.start()

    init_fn(read_q)
    notify_and_join(read_q, readers)
    notify_and_join(write_q, writers)


def parse_word(parser, raw, clean, ref):
    """Return contents of parsed word."""
    parsed = None
    try:
        parsed = parser.parse(raw)
    except Exception as e:
        print(">>>\n" * 3)
        print(f">>> ERROR WHEN PARSING WORD ({ref}):", raw, "<<<")
        print(">>>", [T.uniname(x) for x in raw], "<<<")
        print(e)
        print(">>>\n" * 3)
        return None

    if not "".join(parsed.vowel) or not "".join(parsed.letter):
        # no letters or vowels
        return None

    syllables = parser.syl(parsed).json
    return dict(
        hebrew=clean,
        shemot=grammar.isshemot(clean),
        gematria=grammar.gematria(clean),
        syllen=len(syllables),
        parsed=str(parsed.flat()),
        rules=str(parsed.rules.flat()),
        syls=syllables,
    )


def save_database(lock, pos, write_q):
    """Save books, words, and occurrences to the database."""
    # pylint: disable=too-many-locals
    db_create(app, db)
    tqdm.set_lock(lock)

    book_offset = 0
    word_offset = 0
    known_words = {}
    try:
        book_offset = Book.query.add_columns(func.max(Book.id)).first()[-1] or 0
        word_offset = Word.query.add_columns(func.max(Word.id)).first()[-1] or 0
        known_words = {w.hebrew: w.id for w in Word.query.all()}
    except Exception:
        pass

    word_offset += 1
    parser = grammar.Parser()
    for msg in queuer(write_q):
        books = msg.data["books"]
        words = []
        occur = []

        for book in books:
            book["id"] += book_offset

        desc = f"{os.getpid()} SAVE  {books[0]['name']:<15}"
        for clean, word in tqdm(msg.data["words"].items(), desc=desc, position=pos):
            word_id = known_words.get(clean, word_offset)
            if clean not in known_words:  # new word
                parsed = parse_word(parser, word["raw"], clean, word["ref"])
                if not parsed:
                    continue

                parsed["id"] = word_id
                known_words[clean] = word_id
                word_offset += 1
                words.append(parsed)

            occur.append(
                dict(
                    book_id=word["book_id"] + book_offset,
                    word_id=word_id,
                    ref=word["ref"],
                    freq=word["freq"],
                )
            )

        for obj, values in {Book: books, Word: words, Freq: occur}.items():
            if not values:
                continue
            db.engine.execute(obj.__table__.insert().values(values))


def save_words(lock, pos, write_q):
    """Save words to the database."""
    # pylint: disable=too-many-locals
    db_create(app, db)
    tqdm.set_lock(lock)

    seen = {}
    parser = grammar.Parser()
    for msg in queuer(write_q):
        book_id = msg.data["num"]
        book_name = msg.data["name"]

        # objects to insert into database
        book = {"id": book_id, "name": book_name}
        words = []
        occur = []

        desc = f"{os.getpid()} SAVE  {book_name:<15}"
        for clean, stats in tqdm(msg.data["words"].items(), desc=desc, position=pos):
            word_id = seen.get(clean, len(seen) + 1)
            raw = stats["raw"]
            if clean not in seen:
                seen[clean] = word_id
                parsed = parser.parse(raw)
                if not "".join(parsed.vowel):  # unvowelized word
                    continue

                syllables = parser.syllabify(parsed)
                words.append(
                    dict(
                        id=word_id,
                        hebrew=clean,
                        shemot=grammar.isshemot(clean),
                        gematria=grammar.gematria(clean),
                        parsed=str(parsed.flat()),
                        syllables=str(syllables),
                        syllen=len(syllables),
                        rules=str(parsed.rules.flat()),
                    )
                )

            occur.append(
                dict(
                    book_id=book_id,
                    word_id=word_id,
                    ref=stats["ref"],
                    freq=stats["freq"],
                )
            )

        for obj, values in {Book: book, Word: words, Freq: occur}.items():
            db.engine.execute(obj.__table__.insert().values(values))
