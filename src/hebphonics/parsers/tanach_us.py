#!/usr/bin/env python
# coding: utf-8
"""Download and parse biblical texts from <http://tanach.us/>.

The text is an Unicode XML version of the [Leningrad Codex][1].

[1]: https://en.wikipedia.org/wiki/Leningrad_Codex

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
                    <k>...</k>
                    <q>...</q>
                </v>
            </c>
        </book>
    </tanach>
</Tanach>
```
Relevant structural information:
  - `<c>` chapter
  - `<v>` verse
  - `<w>` word
    - `<s>` size marking (we keep)
    - `<x>` notes (we ignore)
  - `<k>` ketiv (we ignore)
  - `<q>` qere (we keep)
"""
# native
from functools import partial
from multiprocessing import Queue
from pathlib import Path
from typing import List
import os
import re

# lib
from bs4 import BeautifulSoup
from tqdm import tqdm

# pkg
from . import parse_args, download_unzip, Msg, queuer, spawn_processes, save_database
from .. import tokens as T


def get_word(word):
    """Return normalized contents of a word."""
    return "".join([n.string.strip() for n in word.contents if n.name in [None, "s"]])


def count_words(lock, pos: int, read_q: Queue, write_q: Queue):
    """Count words in a book."""
    # pylint: disable=too-many-locals
    tqdm.set_lock(lock)
    for msg in queuer(read_q):
        with open(msg.data) as stream:
            result = {"books": [], "words": {}}

            soup = BeautifulSoup(stream, "xml")
            book = soup.Tanach.tanach.book
            book_name = str(soup.names.find_all("name")[0].string)
            book_num = int(soup.names.number.string)
            result["books"].append(
                dict(id=book_num, name=book_name, corpus="tanach.us")
            )

            desc = f"{os.getpid()} COUNT {book_name:<15}"
            for word in tqdm(book.find_all(["w", "q"]), desc=desc, position=pos):
                # NOTE: We ignore nested <x> and keep nested <s>!
                raw = get_word(word)
                clean = T.strip(raw)
                if clean in result:
                    result["words"][clean]["freq"] += 1
                else:
                    chapter = word.parent.parent["n"]
                    verse = word.parent["n"]
                    ref = f"{book_name} {chapter}:{verse}"
                    result["words"][clean] = dict(
                        book_id=book_num, freq=1, ref=ref, raw=raw
                    )

        write_q.put(Msg("SAVE", result))


def list_books(read_q: Queue, index: Path):
    """Enqueue paths of books to parse."""
    pid = os.getpid()
    desc = f"{pid} list_books"

    xml = BeautifulSoup(index.read_text(), "xml")
    for book in tqdm(xml.find_all("names"), desc=desc, position=0):
        path = index.parent / f"{book.filename.string}.xml"
        read_q.put(Msg("COUNT", path))


def main(argv: List[str] = None):
    """Parse texts from <http://tanach.us>

    Usage: tanach_us.py [download <folder> | -i PATH] [-n COUNT]

    Options:
      download <folder>         download XML files to <folder>
      --index, -i PATH          index file [default: text/tanach.us/TanachIndex.xml]
      --cpus, -n NUM            number of CPUs to use; at least 2 [default: all]
    """
    args = parse_args(main.__doc__ or "", argv)
    num_readers = args["num_readers"]
    num_writers = args["num_writers"]

    if args["download"]:
        url = "http://tanach.us/Books/Tanach.xml.zip"
        folder = Path(args["<folder>"]).resolve()
        pattern = re.compile(r"Books/[^.]+.xml")
        path_index = download_unzip(url, folder, pattern) / "TanachIndex.xml"
    else:
        path_index = Path(args["--index"]).resolve()

    init_fn = partial(list_books, index=path_index)
    spawn_processes(init_fn, count_words, save_database, num_readers, num_writers)


if __name__ == "__main__":  # pragma: no cover
    main()
