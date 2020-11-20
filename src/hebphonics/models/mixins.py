#!/usr/bin/env python
# coding: utf-8

"""Common database mixins."""

# native
from datetime import datetime

# lib
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList


def now():
    """Return a string representation of the current date/time.

    Returns:
        (str): current UTC time as a string
    """
    return str(datetime.utcnow())[:19] + "Z"


def db_create(app, db):
    """Create database tables."""
    with app.app_context():
        db.create_all()
        db.session.commit()


def db_destroy(app, db):
    """Destroy all database tables."""
    with app.app_context():
        db.drop_all()
        db.session.commit()


class BaseMixin:
    """Columns to identify rows and date metadata."""

    id = Column(Integer, primary_key=True)

    # dates are written in ISO8601 format
    created_on = Column(String(20), default=now)
    updated_on = Column(String(20), default=now)
    removed_on = Column(String(20), default="")

    @property
    def json(self):
        """Convert to JSON."""
        return to_json(self, self.__class__)


class UserMixin(BaseMixin):
    """Basic User object from api.auth."""

    # from api.auth
    name = Column(String, default="")
    email = Column(String, unique=True)
    photo = Column(String, default="")


class UserDataMixin(BaseMixin):
    """Table with user-generated data.

    NOTE: Requires a `User` table (e.g., inherit from `UserMixin`).
    """

    @declared_attr
    def user_id(cls):  # pylint: disable=no-self-argument
        """Return the id of row creator."""
        return Column(Integer, ForeignKey("user.id"))

    @declared_attr
    def user(cls):  # pylint: disable=no-self-argument
        """Return the user who created this row."""
        return relationship("User")


def to_json(inst, cls, level=0):
    """Convert SQLAlchemy result to JSON."""
    result = {col.name: getattr(inst, col.name) for col in cls.__table__.columns}

    if level > 0:
        return result

    for rel in cls.__mapper__.relationships:
        val = getattr(inst, rel.key)
        if val == inst:
            result[rel.key] = {
                col.name: getattr(inst, col.name) for col in cls.__table__.columns
            }
        elif hasattr(val, "json"):
            result[rel.key] = to_json(val, val.__class__, level + 1)
        elif isinstance(val, InstrumentedList):
            result[rel.key] = [to_json(v, v.__class__, level + 1) for v in val]
        elif rel.back_populates and val:
            result[rel.key] = [to_json(v, v.__class__, level + 1) for v in val]
        else:
            result[rel.key] = None
    return result
