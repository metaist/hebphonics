#!/usr/bin/python
# coding: utf-8

"""Parser for the Tanach from <http://tanach.us/>."""

#from __future__ import division
import logging
import os
import sys

from bs4 import BeautifulSoup

try:
    from .. import metadata, codes, hebrew, db
except ValueError:  # pragma: no cover
    from hebphonics import metadata, codes, hebrew, db

globals().update(metadata.metadata())  # add package metadata

logger = logging.getLogger(__name__)

BAR_WIDTH = 80  # max width of the
BAR_CHAR = '.'  # character to display

MSG_PARSING = '[%s] parsing...'
MSG_PARSED = '[%s] parsed'


def parse_word(session, xml_word, db_book, location):
    """Parses a word found in a book.

    Args:
        session (Session): database session
        xml_word (BeautifulSoup): xml contents of the word
        db_book (Book): book in which the word was found
        location (str): location in which the word was found
    """
    # <w> can have nested <x>; we use .contents, not .string
    uni_word = xml_word.contents[0]
    stripped = codes.strip(uni_word)

    # see if this word already exists
    db_word = session.query(db.Word)\
                     .filter_by(hebrew=stripped)\
                     .first()
    db_rel = None

    if not db_word:  # need to create word
        syllables = hebrew.syllabify(uni_word)
        db_word = db.Word(hebrew=stripped,
                          syllables=str(syllables))
    else:  # word exists; get occurences
        db_rel = session.query(db.Occurence)\
                        .filter_by(book=db_book, word=db_word)\
                        .first()
    # word exists, although may not have occured in this book

    if db_rel:  # word appeared in book previously
        db_rel.frequency += 1
    else:  # first occurence of this word in this book
        db_rel = db.Occurence(frequency=1, first_pos=location)
        db_rel.word = db_word
        db_book.words.append(db_rel)  # pylint: disable=E1101


def parse_book(session, xml_book):
    """Parses the words found in a book.

    Args:
        session (Session): database session
        xml_book (BeautifulSoup): xml contents of the book
    """
    xml_book = xml_book.Tanach.tanach.book
    name = xml_book.names.find_all('name')[0].string
    logger.info(MSG_PARSING, name)

    db_book = db.Book(name=name)
    session.add(db_book)

    sys.stdout.write('[%s]' % (' ' * BAR_WIDTH))
    sys.stdout.flush()
    sys.stdout.write('\b' * (BAR_WIDTH + 1))

    xml_chapters = xml_book.find_all('c')
    inc = (len(xml_chapters) // BAR_WIDTH) or 1

    for i, xml_chapter in enumerate(xml_chapters):
        if 0 == i % inc:
            sys.stdout.write(BAR_CHAR)
            sys.stdout.flush()

        for xml_verse in xml_chapter.find_all('v'):
            for xml_word in xml_verse.find_all('w'):
                location = xml_chapter['n'] + ':' + xml_verse['n']
                parse_word(session, xml_word, db_book, location)

    sys.stdout.write(BAR_CHAR + '\n')

    session.commit()
    logger.info(MSG_PARSED, name)


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

    xml_books = xml_index.Tanach.find_all('index')[0].books

    for xml_book in xml_books.find_all('names'):
        book_path = os.path.join(root, xml_book.filename.string + '.xml')
        with open(book_path) as stream:
            xml_soup = BeautifulSoup(stream, 'xml')
            parse_book(session, xml_soup)
    logger.info(MSG_PARSED, 'tanach')


if '__main__' == __name__:  # pragma: no cover
    logger = logging.getLogger('hebphonics.parsers.TanachParser')
    logger.info('connecting...')
    parse(db.connect(database=os.path.join('db', 'hebphonics.db')),
          os.path.join('texts', 'tanach.us'))
