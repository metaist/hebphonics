#!/usr/bin/env python
# coding: utf-8
"""Server runner."""

# native
import os

# pkg
from . import app, models


def main():
    """Main entry point."""
    models.db_create(app, models.db)
    app.run(port=int(os.getenv("FLASK_RUN_PORT", "8080")), debug=True)


if __name__ == "__main__":
    main()
