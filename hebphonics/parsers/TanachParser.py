#!/usr/bin/python
# coding: utf-8

"""Parser for the Tanach from <http://tanach.us/>."""

from __future__ import division
from sys import stdout
import logging
import os

from bs4 import BeautifulSoup

try:
    from .. import metadata, codes, hebrew, db
except ValueError:  # pragma: no cover
    from hebphonics import metadata, codes, hebrew, db

globals().update(metadata.metadata())  # add package metadata

logger = logging.getLogger(__name__)

MSG_COUNTING, MSG_COUNTED = '[%s] counting...', '[%s] counted (%d words)'
MSG_PARSING, MSG_PARSED = '[%s] parsing...', '[%s] parsed'
MSG_SAVING, MSG_SAVED = '[%s] saving...', '[%s] saved'


class Progress(object):
    """A basic progress bar."""
    bar = '[- N/A -]'
    width = None

    total = 0

    def __init__(self, total):
        """Construct a new progress bar."""
        self.total = total
        self.width = len(self.bar)

    def start(self):
        """Start the progress bar."""
        stdout.write(self.bar)
        stdout.flush()
        return self

    def update(self, current, total=None):
        """Update progress bar."""
        if total is not None:  # pragma: no cover
            self.total = total

        stdout.write('\b' * self.width)
        stdout.write('[{0: >7.2%}]'.format(current / self.total))
        stdout.flush()
        return self

    def end(self):
        """End the progress bar."""
        stdout.write('\b' * self.width)  # erase progress bar
        stdout.flush()
        return self


def save(session, name, counts):
    """Saves the contents of a book.

    Args:
        session (session): database session
        name (str): the name of the book
        counts (dict): unparsed words mapped to frequency counts
    """
    logger.info(MSG_SAVING, name)

    db_book = db.Book(name=name)

    progress = Progress(len(counts)).start()
    for i, (stripped, (frequency, uni_word)) in enumerate(counts.iteritems()):
        progress.update(i)

        # check if word appeared in different book
        db_word = session.query(db.Word)\
                         .filter_by(hebrew=stripped)\
                         .first()

        if not db_word:  # first occurence of word ever
            groups = hebrew.clusters(uni_word)
            syllables = hebrew.syllabify(groups=groups, strict=True)
            syllables_hatafs = hebrew.syllabify(groups=groups, strict=False)
            db_word = db.Word(hebrew=stripped,
                              gematria=hebrew.gematria(stripped),
                              syllables=str(syllables),
                              syllen=len(syllables),
                              syllen_hatafs=len(syllables_hatafs))

        db_rel = db.Occurence(frequency=frequency)
        db_rel.word = db_word
        db_book.words.append(db_rel)  # pylint: disable=E1101

    session.add(db_book)
    session.commit()

    progress.end()
    logger.info(MSG_SAVED, name)


def count(xml_book):
    """Returns the words and counts in a book.

    Args:
        xml_book (BeautifulSoup): xml contents of the book

    Returns:
        dict. Words mapped to frequency counts.
    """
    result = {}

    xml_book = xml_book.Tanach.tanach.book  # pylint: disable=E1101
    xml_words = xml_book.find_all('w')

    name = xml_book.names.find_all('name')[0].string
    logger.info(MSG_COUNTING, name)

    progress = Progress(len(xml_words)).start()
    for i, xml_word in enumerate(xml_words):
        progress.update(i)

        # <w> can have nested <x>; we use .contents, not .string
        uni_word = xml_word.contents[0]
        stripped = codes.strip(uni_word)

        if stripped in result:
            result[stripped][0] += 1
        else:
            result[stripped] = [1, uni_word]

    progress.end()
    logger.info(MSG_COUNTED, name, len(result))

    return name, result


def parse(session, root, root_file='Tanach.xml'):
    """"Parse the tanach from <tanach.us>.

    Args:
        session (Session): database session
        root (str): directory with tanach files
        root_file (str): name of the "Tanach.xml" file

    Returns:
        dict. Dictionary of words parsed.
    """
    logger.info(MSG_PARSING, 'tanach')

    logger.info(MSG_PARSING, 'index')
    path = os.path.join(root, root_file)
    xml_index = BeautifulSoup(open(path), 'xml')
    logger.info(MSG_PARSED, 'index')

    xml_books = xml_index.Tanach.find_all('index')  # pylint: disable=E1101
    xml_books = xml_books[0].books

    for xml_book in xml_books.find_all('names'):
        book_path = os.path.join(root, xml_book.filename.string + '.xml')
        with open(book_path) as stream:
            xml_soup = BeautifulSoup(stream, 'xml')
            book_name, book_counts = count(xml_soup)
            save(session, book_name, book_counts)

    logger.info(MSG_PARSED, 'tanach')


if '__main__' == __name__:  # pragma: no cover
    logger = logging.getLogger('hebphonics.parsers.TanachParser')
    logger.info('connecting...')
    parse(db.connect(database=os.path.join('db', 'hebphonics.db')),
          os.path.join('texts', 'tanach.us'))
