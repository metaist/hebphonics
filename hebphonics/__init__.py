#!/usr/bin/python
# coding: utf-8

"""Hebrew parsing and word-list building using Python.

HebPhonics is Hebrew language parser that is optimized for teaching Hebrew
reading and fluency.
"""

import logging

from . import metadata

globals().update(metadata.metadata())  # add package metadata

__all__ = ['codes', 'names', 'hebrew']

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(module)s %(message)s')
