#!/usr/bin/env python
"""
keybump
~~~~~~~

manage your versioning like a boss .

  - keybump is an opinionated command-line app to manage versioning workflow + dist + releasing
  - keybump makes following the semantic versioning specification (http://semver.org) a breeze
  - keybump helps to automate the tedious task of summarizing changes from one version to the next by intelligently parsing the commit messages


links:
``````

* `homepage: <http://gregorynicholas.github.io/keybump>`_
* `source: <http://github.com/gregorynicholas/keybump>`_
* `python-package: <http://packages.python.org/keybump>`_
* `travis-ci: <http://travis-ci.org/gregorynicholas/keybump>`_
* `development version: <http://github.com/gregorynicholas/keybump/zipball/master#egg=keybump-dev>`_
* `github-issues: <http://github.com/gregorynicholas/keybump/issues>`_
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

with open("requirements.txt", "r") as f:
  requires = f.readlines()


setup(
  name="keybump",
  version=__version__,
  url="http://github.com/gregorynicholas/keybump",
  author="gregorynicholas",
  author_email="gn@gregorynicholas.com",

  description="manage your versioning like a boss .",
  long_description=__doc__,

  install_requires=requires,

  scripts=[
    'bin/keybump',
  ],

  packages=[
    'keybump',
  ],

  namespace_packages=[
  ],

  py_modules=[
  ],

  test_suite='nose.collector',
  tests_require=[
    'nose',
    'nose-cov',
    'mock',
  ],

  dependency_links=[
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
