#!/usr/bin/env python
"""
  keybump
  ~~~~~~~

  keybump is an opinionated command-line tool to manage versioning, dist, releasing
  package builds.

  keybump makes following the semantic versioning specification (http://semver.org) a breeze.

  keybump helps to automate the tedious task of summarizing changes from one version to the next by intelligently parsing the commit messages.


  links
  -----

* [github docs](http://gregorynicholas.github.com/keybump)
* [docs](http://packages.python.org/keybump)
* [semantic versioning specification](http://semver.org)

"""
from setuptools import setup

__version__ = "3.0.1"

setup(
  name="keybump",
  version=__version__,
  url="http://github.com/gregorynicholas/keybump",
  license="MIT",
  author="gregorynicholas",
  description="helper script to perform a project release, and follow the "
  "semantic versioning specification.",
  long_description=__doc__,
  scripts=["keybump"],
  py_modules=[
    "keybump_config",
    "keybump_formatter",
    "keybump_git_utils",
    "keybump_package_utils",
    "keybump_shell_utils",
  ],
  zip_safe=False,
  platforms="any",
  install_requires=[
    "pyyaml==3.10",
  ],
  tests_require=[
    "nose==1.2.1",
    "mock==1.0.1",
  ],
  dependency_links=[],
  test_suite="keybump_tests",
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
