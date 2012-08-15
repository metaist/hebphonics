#!/usr/bin/python
# coding: utf-8

"""Metadata for HebPhonics package."""

__author__ = 'The Metaist'
__copyright__ = 'Copyright 2012, Metaist'
__email__ = 'metaist@metaist.com'
__license__ = 'MIT'
__maintainer__ = 'The Metaist'
__status__ = 'Prototype'
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)


def metadata():
    """Return a dictionary of package metadata.

    Returns:
        dict. HebPhonics metadata strings.

    >>> type(metadata()) is dict
    True
    """
    fields = map(
        lambda x: '__' + x + '__',
        ['author', 'copyright', 'email', 'license', 'maintainer', 'status',
            'version_info', 'version']
    )

    return dict((f, globals()[f]) for f in fields)
