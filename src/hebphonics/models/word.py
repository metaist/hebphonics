#!/usr/bin/env python
# coding: utf-8
"""Word-related models."""
# pylint: disable=too-few-public-methods

from . import db, BaseMixin


class Book(BaseMixin, db.Model):
    """Hebrew book."""

    name = db.Column(db.String, unique=True)
    freqs = db.relationship("Occurrence", backref="book")


class Word(BaseMixin, db.Model):
    """Hebrew word."""

    hebrew = db.Column(db.Unicode, index=True, unique=True)
    shemot = db.Column(db.Boolean, default=False)
    gematria = db.Column(db.Integer)
    parsed = db.Column(db.String, index=True)
    syllables = db.Column(db.String)
    syllen = db.Column(db.Integer)  # number of syllables
    rules = db.Column(db.String)  # parse rules applied


class Occurrence(BaseMixin, db.Model):
    """Occurrence of a word in a book."""

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"))

    ref = db.Column(db.String)  # first time it appears
    freq = db.Column(db.Integer, default=1)  # how often it appears

    word = db.relationship("Word", backref="freqs")
