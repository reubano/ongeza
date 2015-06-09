#!/usr/bin/env python
"""
  keybump
  ~~~~~~~

  manage your versioning like a boss .

  - keybump is an opinionated command-line app to manage versioning workflow + dist + releasing.
  - keybump makes following the semantic versioning specification (http://semver.org) a breeze.
  - keybump helps to automate the tedious task of summarizing changes from one version to the next by intelligently parsing the commit messages.


  links
  -----

* [source](http://github.com/gregorynicholas/keybump)
* [github docs](http://gregorynicholas.github.io/keybump)
* [python package](http://packages.python.org/keybump)
* [semantic versioning specification](http://semver.org)
* [travis-ci](http://travis-ci.org/gregorynicholas/keybump)

"""
from setuptools import setup

__version__ = "3.0.1"

setup(
  name="keybump",
  version=__version__,
  url="http://github.com/gregorynicholas/keybump",
  license="MIT",
  author="gregorynicholas",
  author_email="gn@gregorynicholas.com",
  description="manage your versioning like a boss .",
  long_description=__doc__,
  scripts=["bin/keybump"],
  py_modules=[
  ],
  packages=[
    'keybump',
  ],
  zip_safe=False,
  platforms="any",
  install_requires=[
    "pyyaml==3.10",
  ],
  test_suite="tests",
  tests_require=[
    "nose==1.2.1",
    "mock==1.0.1",
  ],
  dependency_links=[],
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
