#!/usr/bin/env python
"""
keybump
-----------------------

Helper script to perform a project release, and follow the Semantic Versioning
Specification.

Links
`````

* `documentation <http://packages.python.org/keybump>`_
* `semantic versioning specification <http://semver.org/>`_
* `development version
  <http://github.com/gregorynicholas/keybump/zipball/master#egg=keybump-dev>`_

"""
from setuptools import setup

setup(
  name='keybump',
  version='2.0.2',
  url='http://github.com/gregorynicholas/keybump',
  license='MIT',
  author='gregorynicholas',
  description='Helper script to perform a project release, and follow the \
Semantic Versioning Specification.',
  long_description=__doc__,
  scripts=['keybump.py', 'git-changelog'],
  py_modules=[],
  # packages=['flaskext'],
  zip_safe=False,
  platforms='any',
  install_requires=[
  ],
  tests_require=[
    # 'nose',
  ],
  dependency_links = [
  ],
  # test_suite='nose.collector',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
