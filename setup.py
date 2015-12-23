#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import bump
import pkutils

from os import path as p

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

sys.dont_write_bytecode = True
requirements = list(pkutils.parse_requirements('requirements.txt'))
dependencies = list(pkutils.parse_requirements('requirements.txt', dep=True))
dev_requirements = list(pkutils.parse_requirements('dev-requirements.txt'))
readme = pkutils.read('README.rst')
license = bump.__license__
version = bump.__version__
title = bump.__title__
gh = 'https://github.com/reubano'


setup(
    name=title,
    version=version,
    description=bump.__description__,
    long_description=readme,
    author=bump.__author__,
    author_email=bump.__email__,
    url='%s/%s' % (gh, title),
    download_url='%s/%s/downloads/%s*.tgz' % (gh, title, title),
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependencies,
    test_suite='nose.collector',
    tests_require=dev_requirements,
    license=license,
    zip_safe=False,
    keywords=[title],
    classifiers=[
        pkutils.LICENSES[license],
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
        'Topic :: Software Development :: Version Control',
    ],
    platforms=['MacOS X', 'Windows', 'Linux'],
    scripts=[p.join('bin', 'bump')]
)
