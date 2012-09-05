#!/usr/bin/python
# coding: utf-8

"""HebPhonics database."""

from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.types import Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

from . import metadata

globals().update(metadata.metadata())  # add package metadata

DEFAULT_DB = ':memory:'

# pylint: disable=W0232,R0903
Base = declarative_base()


class Occurence(Base):
    """Occurences of a word in a book."""
    __tablename__ = 'occurences'

    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'), primary_key=True)

    frequency = Column(Integer, default=1)
    word = relationship('Word', backref='occurences')

    def __repr__(self):
        """Return string representation of the class.

        Example:
        >>> repr(Occurence())
        'Occurence(word=None, book=None, frequency=None)'
        """
        result = ('Occurence(word={0.word}, book={0.book}, '
                  'frequency={0.frequency})')
        return result.format(self)


class Book(Base):
    """A Hebrew book."""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    words = relationship('Occurence', backref='book')

    def __repr__(self):
        """Return string representation of the class.

        Example:
        >>> repr(Book())
        'Book(name=None)'
        """
        return ('Book(name={0.name})').format(self)


class Word(Base):
    """A Hebrew word."""
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    hebrew = Column(Unicode, unique=True)
    syllables = Column(String)
    syllen = Column(Integer)  # number of syllables
    syllen_hatafs = Column(Integer)  # number of syllables including hatafs

    def __repr__(self):
        """Return string representation of the class.

        Example:
        >>> repr(Word())
        'Word(hebrew=None, syllables=None, syllen=None, syllen_hatafs=None)'
        """
        result = ('Word(hebrew={0.hebrew!r}, syllables={0.syllables}, '
                  'syllen={0.syllen}, syllen_hatafs={0.syllen_hatafs})')
        return result.format(self)


def connect(database=DEFAULT_DB, debug=False):
    """Returns a SQLAlchemy engine conencted to the given sqlite database.

    Kwargs:
        database (str): sqlite database (default: ":memory:")
        debug (bool): whether to output log statements (default: False)

    Returns:
        Session. Database session.
    """
    engine = create_engine('sqlite:///' + database, echo=debug)
    Base.metadata.create_all(engine)
    return Session(bind=engine)
