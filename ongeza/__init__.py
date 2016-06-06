# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
ongeza
~~~~~~

An automated way to follow the Semantic Versioning Specification

Examples:
    basic usage::

        >>> version = Project().current_version
        >>> version == (version if TRAVIS else __version__)
        True

Attributes:
    DEFAULT_TAG_FMT (str): The default tag format
    DEFAULT_TAG_MSG_FMT (str): The default tag message format
    DEFAULT_COMMIT_MSG_FMT (str): The default commit message format
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

from os import getenv

import semver

from fnmatch import fnmatch
from subprocess import CalledProcessError
from builtins import *

from .git_utils import Git, logger

__version__ = '1.12.0'

__title__ = 'ongeza'
__author__ = 'Reuben Cummings'
__description__ = 'Your Semantic Versioning personal assistant'
__email__ = 'reubano@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Reuben Cummings'

DEFAULT_TAG_FMT = 'v{version}'
DEFAULT_TAG_MSG_FMT = 'Version {version} Release'
DEFAULT_COMMIT_MSG_FMT = 'Bump to version {version}'
TRAVIS = getenv('TRAVIS')


class Project(Git):
    """
    Class representing a project.

    Attributes:
        bumped (bool): Has the project's version been bumped?

        file (str): The file to search for a version.

        version (str): The project's version.

    Args:
        dir_ (str): The project directory (default: None).

        file_ (str): The file to search for a version (default: None).

        version (str): The project's initial version (default: None).

        verbose (bool): Enable verbose logging (default: False).

    Returns:
        New instance of :class:`pygogo.Gogo`

    Examples:
        >>> 'major' in semver.parse(Project().current_version)
        True
    """

    def __init__(self, dir_=None, file_=None, version=None, verbose=False):
        """Initialization method.

        Examples:
            >>> Project()  # doctest: +ELLIPSIS
            <ongeza.Project object at 0x...>
        """
        super(Project, self).__init__(dir_, verbose)
        self.bumped = False
        self.file = file_

        gsed = self.sh('sed --help')
        self.sed = "sed -i" if gsed else "sed -i ''"

        if version:
            self.version = version
        else:
            self.version = self.current_version

    @property
    def current_version(self):
        """The current version parsed from most recent git tag

        Returns:
            str: current version

        Examples:
            >>> semver.parse(Project().current_version)['major'] >= 1
            True
        """
        if self.current_tag:
            version = self.current_tag.lstrip('v')
        else:
            version = None

        if version and not version_is_valid(version):
            version = None

        return version

    @property
    def versions(self):
        """All valid versions parsed from the git tags

        Returns:
            iterator: valid versions

        Examples:
            >>> len(list(Project().versions)) > 1
            True
        """
        versions = (t.lstrip('v') for t in self.tags)
        return filter(version_is_valid, versions)

    def gen_versioned_files(self, wave=1):
        """Generates file names which may contain a version string

        Args:
            wave (int): The set of files to search. Wave 1 includes specific
                files, e.g., 'setup.py', 'bower.json', etc. Wave 2 includes
                general files, e.g., '*.spec', '*.php', '*.py', etc. The best
                practice is to only use wave 2 when wave 1 fails to return a
                versioned file.

        Yields:
            str: file name

        Examples:
            >>> next(Project().gen_versioned_files()) == 'ongeza/__init__.py'
            True
        """
        if self.file:
            yield self.file
        else:
            py_files = ['setup.cfg', 'setup.py', '*/__init__.py']
            js_files = ['bower.json', 'package.json', 'component.json']
            php_files = ['composer.json']
            misc_files = ['*.spec', '*.php', '*.py', '*.xml', '*.json']
            wave_one = py_files + js_files + php_files
            switch = {1: wave_one, 2: misc_files}

            for git_file in self.files:
                if any(fnmatch(git_file, file_) for file_ in switch[wave]):
                    yield git_file

    def set_versions(self, new_version, wave=1):
        if not new_version:
            return

        for file_ in self.gen_versioned_files(wave):
            if not self.version:
                # get all lines in file
                cmd = 'grep -ine "" %s' % file_

                try:
                    lines = self.sh(cmd, True)
                except CalledProcessError:
                    lines = None

                if lines:
                    # escape double quotes
                    escaped = lines.replace('"', '\\"')
                    # find first line containing a version number and the word
                    # 'version'
                    cmd = 'echo "%s" | grep version' % escaped
                    cmd += ' | grep -m1 "[0-9]*\.[0-9]*\.[0-9]*"'

                    try:
                        rep_line = self.sh(cmd, True)
                    except CalledProcessError:
                        cmd = None
                    else:
                        rep_line_num = rep_line.split(':')[0]
                        # replace with new version number
                        cmd = ("%s %ss/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s"
                            % (self.sed, rep_line_num, new_version, file_))
                else:
                    cmd = None
            else:
                # replace current version with new version only if the line
                # contains the word 'version'
                cmd = ("%s '/version/s/%s/%s/g' %s"
                    % (self.sed, self.version, new_version, file_))

            self.sh(cmd) if cmd else None

        self.bumped = self.is_dirty

    def ongeza(self, type_):
        """Bumps a project to a new version

        Args:
            type_ (str): bump type. one of:
                m or major: [x].0.0
                n or minor: x.[y].0
                p or patch: x.y.[z]

        Returns:
            str: new version

        Examples:
            >>> project = Project()
            >>> old_version = semver.parse(project.version)
            >>> new_version = semver.parse(project.ongeza('m'))
            >>> new_version['major'] == old_version['major'] + 1
            True
            >>> new_version = semver.parse(project.ongeza('minor'))
            >>> new_version['minor'] == old_version['minor'] + 1
            True
        """
        switch = {
            'm': semver.bump_major,
            'n': semver.bump_minor,
            'p': semver.bump_patch,
            'major': semver.bump_major,
            'minor': semver.bump_minor,
            'patch': semver.bump_patch}

        new_version = switch.get(type_)(self.version)

        if new_version in set(self.versions):
            self.logger.error('version `%s` already present', new_version)
            new_version = None

        return new_version


def version_is_valid(version):
    """Determines whether a given version meets the semver spec, and if so
    returns the parsed result.

    Args:
        version (str): The version to test

    Returns:
        dict: The parsed version (or an empty dict).

    Examples:
        >>> bool(version_is_valid('1.0.1'))
        True
        >>> bool(version_is_valid('1.0.1')['major'])
        True
        >>> bool(version_is_valid('1.0'))
        False
    """
    try:
        return semver.parse(version)
    except (ValueError, TypeError):
        logger.debug('%s is not a valid version', version)
        return {}
