#!/usr/bin/env python
# coding: utf-8
"""Hebrew phonics tools."""

# __all__ = ["controllers", "models", "parsers", "grammar", "rules", "server", "tokens"]

# native
import os
from pathlib import Path

# lib
from flask import Flask
from dotenv import load_dotenv

# pkg
from .__about__ import (
    __version__,
    __pubdate__,
    __author__,
    __email__,
    __copyright__,
    __license__,
)

load_dotenv()
DB_PATH = Path(os.getenv("DB_NAME", "hebphonics.db")).resolve()

app = Flask(__name__, template_folder="views")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(128).hex())
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# NOTE: do this import now to avoid circular import
# pylint: disable=wrong-import-position, unused-import
from . import models, controllers
