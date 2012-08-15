#!/usr/bin/python
# coding: utf-8

from distutils.core import setup

import hebphonics

setup(name='hebphonics',
      version=hebphonics.__version__,
      author=hebphonics.__author__,
      author_email=hebphonics.__email__,
      url='https://github.com/metaist/hebphonics',
      download_url='https://github.com/metaist/hebphonics',
      description=hebphonics.__doc__.split('\n')[0],
      long_description=hebphonics.__doc__,
      packages=['hebphonics'],
      keywords='hebrew phonics fluency reading',
      license=hebphonics.__license__,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Education',
                   'Topic :: Text Processing',
                   'Topic :: Software Development :: Libraries',
                  ],
     )
