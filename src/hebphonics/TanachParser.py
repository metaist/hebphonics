#!/usr/bin/env python
# coding: utf-8
"""Parse biblical texts from <http://tanach.us/>.

An index file (`TanachIndex.xml`) lists all the books of the bible. Each book
is in a separate XML file (e.g., `Genesis.xml`) and contains both metadata
and textual data.

The relevant structure of a book is:
```xml
<Tanach>
    <tanach>
        <book>
            <c n="...">
                <v n="...">
                    <w>...</w>
                </v>
            </c>
        </book>
    </tanach>
</Tanach>
```

The relevant tags are `<c>` (chapter), `<v>` (verse), and `<w>` (word).
`<w>` tags can contain other special marking tags such as `<s>` (which we
keep) and `<x>` (which we ignore).
"""

# native
from dataclasses import dataclass
from functools import partial
from multiprocessing import Process, RLock, Queue
from pathlib import Path
from typing import Any
import os
import queue

# lib
from bs4 import BeautifulSoup
from tqdm import tqdm


# pkg
from . import grammar, tokens
from .models import db_create, db, Book, Word, Occurrence
from .server import app

N_READERS = os.cpu_count() - 1
N_WRITERS = 1

ROOT_PATH = Path("text") / "tanach.us"
ROOT_FILE = "TanachIndex.xml"


@dataclass
class Msg:
    """Message."""

    kind: str = ""
    data: Any = None


def queuer(q):
    """Queue wrapper."""
    while True:
        try:
            msg = q.get(block=True, timeout=0.05)
            if msg.kind == "END":
                break
            yield msg
        except queue.Empty:
            continue


def save_words(lock, pos, write_q):
    """Save words to the database."""
    # pylint: disable=too-many-locals
    db_create(app, db)
    tqdm.set_lock(lock)

    seen = {}
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
            if clean not in seen:
                seen[clean] = word_id
                parser = grammar.Parser(stats["raw"])
                parsed = parser.parse()
                syllables = parser.syllabify()
                words.append(
                    dict(
                        id=word_id,
                        hebrew=clean,
                        shemot=grammar.isshemot(clean),
                        gematria=grammar.gematria(clean),
                        parsed=str(parsed),
                        syllables=str(syllables),
                        syllen=len(syllables),
                        rules=str(parser.rules),
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

        for obj, values in {Book: book, Word: words, Occurrence: occur}.items():
            db.engine.execute(obj.__table__.insert().values(values))


def get_word(word):
    """Return normalized contents of a word."""
    return "".join([n.string.strip() for n in word.contents if n.name in [None, "s"]])


def count_words(lock, pos, read_q, write_q):
    """Count words in a book."""
    # pylint: disable=too-many-locals
    tqdm.set_lock(lock)
    for msg in queuer(read_q):
        with open(msg.data) as stream:
            stats = {}
            soup = BeautifulSoup(stream, "xml")
            book = soup.Tanach.tanach.book
            book_name = str(soup.names.find_all("name")[0].string)
            book_num = int(soup.names.number.string)

            desc = f"{os.getpid()} COUNT {book_name:<15}"
            for word in tqdm(book.find_all("w"), desc=desc, position=pos):
                # NOTE: We ignore nested <x> and keep nested <s>!
                raw = get_word(word)
                clean = tokens.strip(raw)
                if clean in stats:
                    stats[clean]["freq"] += 1
                else:
                    chapter = word.parent.parent["n"]
                    verse = word.parent["n"]
                    ref = f"{book_name} {chapter}:{verse}"
                    stats[clean] = {"freq": 1, "ref": ref, "raw": raw}

        write_q.put(Msg("SAVE", {"num": book_num, "name": book_name, "words": stats}))


def list_books(read_q, root, root_file):
    """List the books to parse."""
    pid = os.getpid()
    desc = f"{pid} list_books"

    xml_index = BeautifulSoup((root / root_file).read_text(), "xml")
    for xml_book in tqdm(xml_index.find_all("names"), desc=desc, position=0):
        book_path = root / f"{xml_book.filename.string}.xml"
        read_q.put(Msg("COUNT", book_path))


def main():
    """Main entry point."""
    tqdm.set_lock(RLock())

    L_READERS = list(range(N_READERS + 1, N_WRITERS, -1))
    L_WRITERS = list(range(N_WRITERS, 0, -1))
    read_q, write_q = Queue(), Queue()
    readers = [
        Process(
            daemon=True,
            target=partial(count_words, tqdm.get_lock(), i, read_q, write_q),
        )
        for i in L_READERS
    ]
    writers = [
        Process(daemon=True, target=partial(save_words, tqdm.get_lock(), i, write_q))
        for i in L_WRITERS
    ]

    for p in readers + writers:
        p.start()

    list_books(read_q, ROOT_PATH, ROOT_FILE)
    for _ in range(N_READERS):
        read_q.put(Msg(kind="END"))
    for p in readers:
        p.join()

    for _ in range(N_WRITERS):
        write_q.put(Msg(kind="END"))
    for p in writers:
        p.join()


if __name__ == "__main__":  # pragma: no cover
    main()
