#!/usr/bin/python
# coding: utf-8

"""Parsers for specific Hebrew corpora."""

from .. import metadata

globals().update(metadata.metadata())  # add package metadata

__all__ = ['TanachParser']
