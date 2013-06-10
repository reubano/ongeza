#!/usr/bin/env python
"""
  keybump
  ~~~~~~~

  helper script to perform a project release, and follow the semantic
  versioning specification.

  links
  -----

* [github docs](http://gregorynicholas.github.com/keybump)
* [docs](http://packages.python.org/keybump)
* [semantic versioning specification](http://semver.org)

"""
from setuptools import setup

# grab requirments.
with open("requirements.txt") as f:
  required = f.readlines()

setup(
  name="keybump",
  version="3.0.1",
  url="http://github.com/gregorynicholas/keybump",
  license="MIT",
  author="gregorynicholas",
  description="helper script to perform a project release, and follow the "
  "semantic versioning specification.",
  long_description=__doc__,
  scripts=["keybump"],
  zip_safe=False,
  platforms="any",
  install_requires=required,
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
