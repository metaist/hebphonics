#!/usr/bin/env python
# coding: utf-8
"""Database models."""

__all__ = ["user", "word"]

# lib
from flask_sqlalchemy import SQLAlchemy

# pkg
from .. import app
from .mixins import (
    now,
    db_create,
    db_destroy,
    BaseMixin,
    UserMixin,
    UserDataMixin,
    to_json,
)

db = SQLAlchemy(app)

# NOTE: do this import now to avoid circular import
# pylint: disable=wrong-import-position
from .user import User, OAuth
from .word import Book, Word, Occurrence
