#!/usr/bin/python
# coding: utf-8

"""HebPhonics database."""

from sqlalchemy import create_engine, Table, Column, ForeignKey, \
    Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from . import metadata

globals().update(metadata.metadata())  # add package metadata

# pylint: disable=W0232,R0903
Base = declarative_base()  # pylint: disable=C0103


class Corpus(Base):
    """A Hebrew corpus."""
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True)
    name = Column(String)


WORDS_LOCATIONS = Table(
    'words_locations', Base.metadata,
    Column('word_id', Integer, ForeignKey('words.id')),
    Column('location_id', Integer, ForeignKey('locations.id'))
)


class Word(Base):
    """A Hebrew word."""
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    hebrew = Column(Unicode)
    syllables = Column(String)
    syllen = Column(Integer)  # number of syllables
    syllen_hatafs = Column(Integer)  # number of syllables including hatafs

    locations = relationship('Location', secondary=WORDS_LOCATIONS,
                             backref='words')


class Location(Base):
    """A textual reference."""
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    text_id = Column(Integer, ForeignKey('texts.id'))
    chapter = Column(String)
    line = Column(String)

    text = relationship('Text', backref=backref('locations', order_by=id))


def connect(path=':memory:'):
    """Returns a SQLAlchemy engine conencted to the given sqlite database.

    Kwargs:
        path (str): path to sqlite database (default: ":memory:")

    Returns:
        sessionmaker. An object than can create database sessions.
    """
    engine = create_engine('sqlite:///' + path, echo=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
