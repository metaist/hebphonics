#!/usr/bin/env python
# coding: utf-8
"""Login controllers."""

# native
import os

# lib
from flask import redirect, request, session, url_for, make_response
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import current_user, login_user, logout_user, LoginManager

# pkg
from .. import app
from ..models import db, User, OAuth, now

login_manager = LoginManager(app)
login_manager.login_view = "google.login"

blueprint = make_google_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="index",
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
)
app.register_blueprint(blueprint, url_prefix="/login")


@login_manager.user_loader
def load_user(user_id):
    """Return User object from a stored user id.

    Args:
        user_id (unicode): stored user id

    Returns:
        (User): user corresponding to this id or None if none is found.
    """
    return User.query.get(int(user_id))


@oauth_authorized.connect_via(blueprint)
def logged_in(context, token):
    """Create a new user, if necessary, on successful OAuth login.

    Args:
        context (OAuth2ConsumerBlueprint): blueprint context
        token (dict): OAuth token

    Returns:
        (bool): always False to indicate that we create users ourselves.
    """
    resp = context.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return False

    changes = []
    info = resp.json()

    email = info.get("email", "")
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User()
    # user exists

    mapping = {"name": "name", "email": "email", "photo": "picture", "google_id": "id"}
    for attr, key in mapping.items():
        val = info.get(key)
        if getattr(user, attr) != val:
            setattr(user, attr, val)
            user.updated_on = now()

    changes.append(user)
    # always update the user with the latest

    google_id = str(info.get("id", ""))
    oauth = OAuth.query.filter_by(
        provider=context.name, provider_user_id=google_id
    ).first()
    if not oauth:
        oauth = OAuth(provider=context.name, provider_user_id=google_id, token=token)
        oauth.user = user
        changes.append(oauth)
    # oauth token exists

    if changes:
        db.session.add_all(changes)
        db.session.commit()
    login_user(user)

    next_url = session.get("next_url")
    if next_url:
        session["next_url"] = ""
        return redirect(next_url)
    return False


@app.route("/login")
def login():
    """Login with Google."""
    next_url = session.get("next_url") or request.args.get("next_url")

    if not current_user.is_active or not google.authorized:  # not logged in
        print(f"not logged in: {next_url}")
        if next_url:
            session["next_url"] = next_url
        return redirect(url_for("google.login"))

    # logged in
    if next_url:
        session["next_url"] = ""
        resp = make_response(redirect(next_url))
    else:
        resp = make_response(redirect(url_for("index")))  # pragma: no cover
    return resp


@app.route("/logout")
def logout():
    """Log out of the system and go to the homepage."""
    resp = make_response(redirect(url_for("index")))
    logout_user()
    return resp
