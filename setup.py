from distutils.core import setup
import sys

sys.path.append('hebphonics')
import hebphonics

setup(name='hebphonics',
      version='0.0.1',
      author='The Metaist',
      author_email='metaist@metaist.com',
      url='https://github.com/metaist/hebphonics',
      download_url='https://github.com/metaist/hebphonics',
      description='Easy Hebrew language parsing and building word lists using Python.',
      long_description=hebphonics.HebPhonics.__doc__,
      package_dir={'': 'hebphonics'},
      py_modules=['hebphonics'],
      provides=['hebphonics'],
      keywords='hebrew phonics fluency reading',
      license='MIT License',
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
