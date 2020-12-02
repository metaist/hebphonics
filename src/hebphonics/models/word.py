#!/usr/bin/env python
# coding: utf-8
"""Word-related models."""
# pylint: disable=too-few-public-methods

from . import db, BaseMixin


class Book(BaseMixin, db.Model):
    """Hebrew text."""

    name = db.Column(db.String)
    corpus = db.Column(db.String)
    freqs = db.relationship("Freq", backref="book")


class Word(BaseMixin, db.Model):
    """Hebrew word."""

    hebrew = db.Column(db.Unicode, index=True, unique=True)
    shemot = db.Column(db.Boolean, default=False)
    gematria = db.Column(db.Integer)
    syllen = db.Column(db.Integer)  # number of syllables
    parsed = db.Column(db.String, index=True)
    rules = db.Column(db.String)  # parse rules applied
    syls = db.Column(db.JSON)


class Freq(BaseMixin, db.Model):
    """Word in a text."""

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"))

    ref = db.Column(db.String)  # first time it appears
    freq = db.Column(db.Integer, default=1)  # how often it appears

    word = db.relationship(Word, backref="freqs")
