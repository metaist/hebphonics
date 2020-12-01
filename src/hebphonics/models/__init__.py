#!/usr/bin/env python
# coding: utf-8
"""Database models."""

__all__ = ["user", "word"]

# native
import re

# lib
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

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
regexp = lambda expr, item: re.search(expr, item, re.I + re.U) is not None


@sqlalchemy.event.listens_for(sqlalchemy.engine.Engine, "connect")
def sqlite_engine_connect(conn, _):
    """Define regex function."""
    conn.create_function("regexp", 2, regexp)


# NOTE: do this import now to avoid circular import
# pylint: disable=wrong-import-position
from .user import User, OAuth
from .word import Book, Word, Occurrence
