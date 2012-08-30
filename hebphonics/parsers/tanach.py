#!/usr/bin/python
# coding: utf-8

"""Parser for the Tanach from <http://tanach.us/>."""

import os

from bs4 import BeautifulSoup

try:
    from .. import metadata, codes, hebrew
except ValueError:  # pragma: no cover
    from hebphonics import metadata, codes, hebrew

globals().update(metadata.metadata())  # add package metadata


def parse_book(book_xml, previous=None):
    """Returns the words found in a book.

    Args:
        book_xml (BeautifulSoup): xml contents of the book

    Kwargs:
        previous (dict): a dictionary of previous results

    Returns:
        dict. An updated dictionary of results.
    """
    result = (previous or {})

    book = book_xml.Tanach.tanach.book
    print 'Parsing {0}...'.format(book.names.find_all('name')[0].string)
    for chapter in book.find_all('c'):
        for verse in chapter.find_all('v'):
            for word in verse.find_all('w'):
                word_uni = word.contents[0]
                stripped = codes.strip(word_uni)
                if stripped not in result:
                    parsed = hebrew.syllabify(word_uni)
                    result[stripped] = [parsed, 1]
                else:
                    result[stripped][1] += 1

    print '... total words: {0}'.format(len(result))
    return result


def parse_tanach(root, index_xml):
    """Returns the words found in the Tanach.

    Args:
        root (str): directory containing Tanach files
        index_xml (BeautifulSoup): xml contents of the Tanach index

    Returns:
        dict. Dictionary of words found.
    """
    result = {}

    for book in index_xml.Tanach.find_all('index')[0].books.find_all('names'):
        with open(os.path.join(root, book.filename.string + '.xml')) as stream:
            result = parse_book(BeautifulSoup(stream, 'xml'), result)

    return result


def parse(root, root_file='Tanach.xml'):
    """"Parse the tanach from <tanach.us>.

    Args:
        root (str): directory with tanach files
        root_file (str): name of the "Tanach.xml" file

    Returns:
        dict. Dictionary of words parsed.
    """
    path = os.path.join(root, root_file)
    return parse_tanach(root, BeautifulSoup(open(path), 'xml'))


if '__main__' == __name__:  # pragma: no cover
    parse(os.path.join('texts', 'tanach.us'))
