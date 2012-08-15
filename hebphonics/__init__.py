#!/usr/bin/python
# coding: utf-8

"""Hebrew parsing and word-list building using Python.

HebPhonics is Hebrew language parser that is optimized for teaching Hebrew
reading and fluency.
"""

import hebphonics

globals().update(hebphonics.metadata())  # add package metadata

__all__ = ['codes', 'names']
