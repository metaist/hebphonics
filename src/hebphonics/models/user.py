#!/usr/bin/env python
# coding: utf-8
"""User-related models."""

# lib
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin

# pkg
from . import db, now, to_json


class User(UserMixin, db.Model):
    """Represents an authorized user."""

    id = db.Column(db.Integer, primary_key=True)

    # from Google OAuth
    name = db.Column(db.String, default="")
    email = db.Column(db.String, unique=True)
    photo = db.Column(db.String, default="")
    google_id = db.Column(db.String, default="")

    is_blocked = db.Column(db.String, default="N")

    created_on = db.Column(db.String(20), default=now)
    updated_on = db.Column(db.String(20), default=now)

    @staticmethod
    def from_oauth(info):
        """Create a User object from OAuth information.

        Args:
            info (dict): information from OAuth

        Returns:
            (User): new user object
        """
        return User(
            name=info.get("name"),
            email=info.get("email"),
            photo=info.get("picture"),
            google_id=info.get("id"),
            created_on=now(),
        )

    @property
    def json(self):
        """Convert to JSON."""
        return to_json(self, self.__class__)


class OAuth(OAuthConsumerMixin, db.Model):
    """Represents tokens from OAuth."""

    __tablename__ = "oauth"

    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    @property
    def json(self):
        """Convert to JSON."""
        return to_json(self, self.__class__)
