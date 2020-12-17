#!/usr/bin/env python
# coding: utf-8
"""Download and parse Tanakh from <http://mechon-mamre.org/>.

The text is based on the [Aleppo Codex][1].

[1]: https://en.wikipedia.org/wiki/Aleppo_Codex

Each book is in a separate HTML file (e.g., `c01.htm`) and contains navigation
and textual data.

The relevant structure is:
```html
<BODY>
  <H1>...</H1>
  <P>
    <B>...,...</B> ...
  </P>
</BODY>
```

Notes:
  - verses are newline-delimited
  - `<H1>` Hebrew book name
  - `<B>` comma-separated Hebrew numbering of chapter and verse
    - for multipart volumes (e.g., Samuel, Kings) also contains the part number
  - `<BIG>`, `<SMALL>`, `<SUP>` around specific letter (we keep)
  - `<A...>...</A>` links to notes (we ignore)
  - `<BR>` within the text indicates a line break (we replace with a space)
  - `{...}<BR>` indicates `pe` break (we ignore)
  - `{...}` indicates `samekh` break (we ignore)
  - `(...)` indicates the qere (we keep)
    - the unvowelized previous word is the ketiv (we ignore)
"""
# native
from functools import partial
from multiprocessing import Queue
from pathlib import Path
from typing import List
import os
import re

# lib
from tqdm import tqdm

# pkg
from . import parse_args, download_unzip, Msg, queuer, spawn_processes, save_database
from .. import tokens as T, grammar

BOOK_NAMES = {
    "בראשית": "Genesis",
    "שמות": "Exodus",
    "ויקרא": "Leviticus",
    "במדבר": "Numbers",
    "דברים": "Deuteronomy",
    #
    "יהושוע": "Joshua",
    "שופטים": "Judges",
    "שמואל א": "I Samuel",
    "שמואל ב": "II Samuel",
    "מלכים א": "I Kings",
    "מלכים ב": "II Kings",
    "ישעיהו": "Isaiah",
    "ירמיהו": "Jeremiah",
    "יחזקאל": "Ezekiel",
    "הושע": "Hosea",
    "יואל": "Joel",
    "עמוס": "Amos",
    "עובדיה": "Obadiah",
    "יונה": "Jonah",
    "מיכה": "Micah",
    "נחום": "Nahum",
    "חבקוק": "Habakkuk",
    "צפניה": "Zephaniah",
    "חגיי": "Haggai",
    "זכריה": "Zechariah",
    "מלאכי": "Malachi",
    #
    "תהילים": "Psalms",
    "משלי": "Proverbs",
    "איוב": "Job",
    "שיר השירים": "Song of Songs",
    "רות": "Ruth",
    "איכה": "Lamentations",
    "קוהלת": "Ecclesiastes",
    "אסתר": "Esther",
    "דנייאל": "Daniel",
    "עזרא / נחמיה ע": "Ezra",
    "עזרא / נחמיה נ": "Nehemiah",
    "דברי הימים א": "I Chronicles",
    "דברי הימים ב": "II Chronicles",
}


def count_words(lock, pos: int, read_q: Queue, write_q: Queue):
    """Count words in a book."""
    # pylint: disable=too-many-locals
    tqdm.set_lock(lock)
    re_remove = re.compile(
        r"</?P>|</?BIG>|</?SMALL>|</?SUP>|<A[^>]+>(.*)</A>|\{.\}|\(|\)"
    )
    re_name = re.compile(r"<H1>(.*)</H1>")
    re_ref = re.compile(r"<B>(.*)</B>")
    for msg in queuer(read_q):
        result = {"books": [], "words": {}}

        book = Path(msg.data)
        text = book.read_text()
        # book_num = int(book.stem[1:], 10)
        book_name = re_name.search(text)[1]
        book_num = 0
        en_name = ""

        # result["books"].append(
        #     dict(id=book_num, name=book_name, corpus="mechon-mamre.org")
        # )

        save_ref = ""
        desc = f"{os.getpid()} COUNT {book_name:<15}"
        for line in tqdm(text.split("\n"), desc=desc, position=pos):
            line = re_remove.sub("", line).replace("<BR>", " ").strip()
            if save_ref:
                ref, save_ref = save_ref, ""
            else:
                if not line or not line.startswith("<B>"):
                    continue

                ref = re_ref.search(line)[1].replace(" ׆", "")
                if "-" in ref:
                    ref, save_ref = ref.split("-")
                    save_ref = f'{ref.split(",")[0]},{save_ref}'

            ref = f"{book_name} {ref}"
            he_name, ref = ref.rsplit(" ", 1)
            tmp_name = BOOK_NAMES[he_name]
            if tmp_name != en_name:
                en_name = tmp_name
                book_num = list(BOOK_NAMES).index(he_name) + 1
                result["books"].append(
                    dict(id=book_num, name=en_name, corpus="mechon-mamre.org")
                )

            chapter, verse = ref.split(",")
            chapter, verse = grammar.gematria(chapter), grammar.gematria(verse)
            line = re_ref.sub("", line)  # reference removed

            line = line.replace(T.PUNCTUATION_MAQAF, T.PUNCTUATION_MAQAF + " ")
            for raw in line.split():
                clean = T.strip(raw)
                if not clean:
                    continue

                if clean in result["words"]:
                    result["words"][clean]["freq"] += 1
                else:
                    ref = f"{en_name} {chapter}:{verse}"
                    result["words"][clean] = dict(
                        book_id=book_num, freq=1, ref=ref, raw=raw
                    )
        write_q.put(Msg("SAVE", result))


def list_books(read_q: Queue, folder: Path):
    """Enqueue paths of books to parse."""
    for path in sorted(folder.iterdir()):
        read_q.put(Msg("COUNT", path))


def main(argv: List[str] = None):
    """Parse texts from <http://mechon-mamre.org>.

    Usage: mechon_mamre_org.py [download <folder> | -i <PATH>] [-n COUNT]

    Options:
      download <folder>         download HTML files to <folder>
      --index, -i PATH          HTML folder [default: text/mechon-mamre.org]
      --cpus, -n NUM            number of CPUs to use; at least 2 [default: all]
    """
    args = parse_args(main.__doc__ or "", argv)
    num_readers = args["num_readers"]
    num_writers = args["num_writers"]

    if args["download"]:
        url = "http://mechon-mamre.org/htmlzips/ct005.zip"
        folder = Path(args["<folder>"]).resolve()
        pattern = re.compile(r"c/ct/c[0-9]{2}.htm")
        folder = download_unzip(url, folder, pattern)
    else:
        folder = Path(args["--index"]).resolve()

    init_fn = partial(list_books, folder=folder)
    spawn_processes(init_fn, count_words, save_database, num_readers, num_writers)


if __name__ == "__main__":  # pragma: no cover
    main()
