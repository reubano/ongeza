#!/usr/bin/env python
"""
keybump
~~~~~~~

manage your versioning like a boss .

  - keybump is an opinionated command-line app to manage versioning workflow + dist + releasing.
  - keybump makes following the semantic versioning specification (http://semver.org) a breeze.
  - keybump helps to automate the tedious task of summarizing changes from one version to the next by intelligently parsing the commit messages.


links:
``````

* `docs: <http://gregorynicholas.github.io/keybump>`_
* `source: <http://github.com/gregorynicholas/keybump>`_
* `issues: <http://github.com/gregorynicholas/keybump/issues>`_
* `package: <http://packages.python.org/keybump>`_
* `travis-ci: <http://travis-ci.org/gregorynicholas/keybump>`_
* `development version: <http://github.com/gregorynicholas/keybump/zipball/master#egg=keybump-dev>`_
* `semantic versioning specification: <http://semver.org>`_

"""
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

from os import path, listdir
import fnmatch as fm
import re


# parse version number
with open('keybump/__init__.py', 'r') as f:
  v = re.findall(r'__version__\s*=\s*\'(.*)\'', f.read())
  __version__ = v[0]


setup(
  name="keybump",
  version=__version__,
  url="http://github.com/gregorynicholas/keybump",
  author="gregorynicholas",
  author_email="gn@gregorynicholas.com",

  description="manage your versioning like a boss .",
  long_description=__doc__,

  install_requires=[
    'pyyaml==3.10',
    'shell==1.0.1',
  ],

  scripts=[
    'bin/keybump',
  ],

  py_modules=[
  ],

  packages=[
    'keybump',
  ],

  # test_suite="tests",
  test_suite='nose.collector',
  tests_require=[
    'nose==1.2.1',
    'nose-cov',
    'mock==1.0.1',
  ],

  license='MIT',
  zip_safe=False,
  platforms='any',
  classifiers=[
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
