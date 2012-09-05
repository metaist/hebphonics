#!/usr/bin/python
# coding: utf-8

import unittest

from sqlalchemy.orm.session import Session

from hebphonics import db


class TestDB(unittest.TestCase):
    session = None

    def setUp(self):
        """Setup connection."""
        self.session = db.connect(database=db.DEFAULT_DB)

    def test_connect(self):
        """Expected to return a session."""
        test = self.session
        self.assertTrue(test is not None)
        self.assertTrue(isinstance(test, Session))

    def test_model_basic_add(self):
        """Expected to perform basic addition."""
        book1 = db.Book(name="book1")
        occurrence1 = db.Occurence(frequency=5)
        word = db.Word(hebrew=u"example")
        occurrence1.word = word
        book1.words.append(occurrence1)

        self.session.add(book1)
        self.session.commit()

    def test_model_word_accross_books(self):
        """Expected to add the same word to multiple books."""

        book1 = db.Book(name="book1")
        occurrence1 = db.Occurence(frequency=5)
        word = db.Word(hebrew=u"example")
        occurrence1.word = word
        book1.words.append(occurrence1)

        self.session.add(book1)
        self.session.commit()

        book2 = db.Book(name="book2")
        occurrence2 = db.Occurence(frequency=5)
        occurrence2.word = word  # same word!
        book2.words.append(occurrence2)

        self.session.add(book2)
        self.session.commit()
