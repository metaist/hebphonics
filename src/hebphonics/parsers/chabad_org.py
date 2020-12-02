#!/usr/bin/env python
# coding: utf-8
"""Download and parse Tanakh from <https://chabad.org/>.

Each chapter is in a separate HTML file (e.g., `01 - Genesis - 001.html`) and contains
navigation and textual information.

The relevant structure is:
```
<h1>...</h1>
<table class="Co_TanachTable">
  <tr class="Co_Verse">
    <td class="hebrew">
      <a class="co_VerseNum">...</a><span class="co_VerseText">...</span>
    </td>
  </tr>
</table>
```

Notes:
  - `<h1>` contains the name of the book and chapter
  - `<a.co_VerseNum>` is the Hebrew letter value of the verse number
  - `<span.co_VerseText>` contains the text of the Hebrew verse
    - `<span.instructional.ksiv>` indicates the ketiv (we ignore)
    - ketiv is occasionally indicated with parenthesis or brackets (we ignore)
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
import requests


# pkg
from . import (
    Msg,
    parse_args,
    queuer,
    save_database,
    spawn_processes,
    USER_AGENT,
)
from .. import tokens as T

BOOK_NAMES = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    #
    "Joshua",
    "Judges",
    "I Samuel",
    "II Samuel",
    "I Kings",
    "II Kings",
    "Isaiah",
    "Jeremiah",
    "Ezekiel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    #
    "Psalms",
    "Proverbs",
    "Job",
    "Song of Songs",
    "Ruth",
    "Lamentations",
    "Ecclesiastes",
    "Esther",
    "Daniel",
    "Ezra",
    "Nehemiah",
    "I Chronicles",
    "II Chronicles",
]


def get_words(line):
    """Return words from verse."""
    line = (
        line.replace(T.PUNCTUATION_MAQAF, T.PUNCTUATION_MAQAF + " ")
        .replace(":", T.PUNCTUATION_SOF_PASUQ)
        .replace("|", "")  # Should be `paseq`, but we don't want that either.
        .replace(" " + T.POINT_QAMATS + " ", T.POINT_QAMATS + " ")  # Ruth 1:9
        .replace("\n" + T.POINT_HOLAM, T.POINT_HOLAM)  # Esther 3:1
    )
    line = re.sub(r"[\(\[][^)\]]+[\]\)]", "", line)
    return line.strip().split()


def count_words(lock, pos: int, read_q: Queue, write_q: Queue):
    """Count words in a book."""
    tqdm.set_lock(lock)
    for msg in queuer(read_q):
        result = {"books": [], "words": {}}

        book = BeautifulSoup(Path(msg.data).read_text(), "lxml").find("text")
        book_id = int(book["num"])
        result["books"].append(dict(id=book_id, name=book["name"]))

        desc = f"{os.getpid()} COUNT {book['name']:<15}"
        for line in tqdm(book.find_all("line"), desc=desc, position=pos):
            for raw in get_words(line.string):
                clean = T.strip(raw)
                if not clean:
                    continue

                if clean in result["words"]:
                    result["words"][clean]["freq"] += 1
                else:
                    ref = line["ref"]
                    result["words"][clean] = dict(
                        book_id=book_id, freq=1, ref=ref, raw=raw
                    )

        write_q.put(Msg("SAVE", result))


def list_books(read_q: Queue, folder: Path):
    """Enqueue paths of books to parse."""
    for path in sorted(folder.iterdir()):
        read_q.put(Msg("COUNT", str(path)))


def download(folder: Path):
    """Download the corpus to the given `folder`."""
    # pylint: disable=too-many-locals
    folder.mkdir(parents=True, exist_ok=True)

    tagstr = lambda t: " ".join(
        [e.string.strip() for e in t.contents if e.name is None]
    )

    def _get_xml(info):
        result = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n"""
        result += (
            f'<text corpus="chabad.org" num="{info["num"]}" name="{info["name"]}">\n'
        )
        for line in info["lines"]:
            result += f'  <line ref="{line["ref"]}">{line["text"]}</line>\n'
        result += "</text>\n"
        return result

    url_base = "https://www.chabad.org"
    next_url = f"{url_base}/library/bible_cdo/aid/8165"
    book = {}
    book_path = None
    while next_url:
        res = requests.get(next_url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(res.text, "html.parser")
        next_url = soup.find(rel="next")
        if not next_url or next_url["href"] == "/article.asp?aid=0":
            next_url = None
        else:
            next_url = f"{url_base}{next_url['href']}"

        h1 = soup.find("h1").string.split(" - ")
        book_name, chapter = h1[-2], int(h1[-1].split(" ")[-1])
        book_num = BOOK_NAMES.index(book_name) + 1

        if book_num != book.get("num"):  # new book
            if book and book_path:
                book_path.write_text(_get_xml(book))
                print(f"downloaded {book_path}")
            book = dict(num=book_num, name=book_name, lines=[])
            book_path = folder / f"{book_num:02}-{book_name}.xml"

        verses = soup.find_all("tr", class_="Co_Verse")
        for verse in tqdm(verses, desc=f"{chapter:03} {book_name:<15}"):
            verse_num = int(verse.find(class_="co_VerseNum").string)
            verse = verse.find(class_="hebrew").find(class_="co_VerseText")
            book["lines"].append(
                dict(ref=f"{book_name} {chapter}:{verse_num}", text=tagstr(verse))
            )

    if book and book_path:
        book_path.write_text(_get_xml(book))
        print(f"downloaded {book_path}")


def main(argv: List[str] = None):
    """Parse texts from <https://www.chabad.org>.

    Usage: chabad_org.py [download <folder> | -i <PATH>] [-n COUNT]

    Options:
      download <folder>         download HTML files to <folder>
      --index, -i PATH          HTML folder [default: text/chabad.org]
      --cpus, -n NUM            number of CPUs to use; at least 2 [default: all]
    """
    args = parse_args(main.__doc__ or "", argv)
    num_readers = args["num_readers"]
    num_writers = args["num_writers"]

    if args["download"]:
        folder = Path(args["<folder>"]).resolve()
        download(folder)
    else:
        folder = Path(args["--index"]).resolve()

    init_fn = partial(list_books, folder=folder)
    spawn_processes(init_fn, count_words, save_database, num_readers, num_writers)


if __name__ == "__main__":  # pragma: no cover
    main()
