# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
ongeza
~~~~~~

An automated way to follow the Semantic Versioning Specification

Examples:
    basic usage::

        >>> Project().current_version in {__version__, '1.2.0'}
        True

Attributes:
    DEFAULT_TAG_FMT (str): The default tag format
    DEFAULT_TAG_MSG_FMT (str): The default tag message format
    DEFAULT_COMMIT_MSG_FMT (str): The default commit message format
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import semver
import pygogo as gogo

from fnmatch import fnmatch
from subprocess import CalledProcessError
from builtins import *

from .git_utils import Git

__version__ = '1.8.2'

__title__ = 'ongeza'
__author__ = 'Reuben Cummings'
__description__ = 'Your Semantic Versioning personal assistant'
__email__ = 'reubano@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Reuben Cummings'

DEFAULT_TAG_FMT = 'v{version}'
DEFAULT_TAG_MSG_FMT = 'Version {version} Release'
DEFAULT_COMMIT_MSG_FMT = 'Bump to version {version}'

logger = gogo.Gogo(__name__).logger


class Project(Git):
    """
    class representing a project object.
    """

    def __init__(self, dir_=None, file_=None, version=None, verbose=False):
        """
        Parameters
        ----------
        dir : str
            the project directory

        file_ : str
            the file to search for a version

        Examples
        --------
        >>> Project()  # doctest: +ELLIPSIS
        <ongeza.Project object at 0x...>
        """
        super(Project, self).__init__(dir_, verbose)
        self.bumped = False
        self.file = file_

        if version:
            self.version = version
        else:
            self.version = self.current_version

    @property
    def current_version(self):
        """
        :returns: string of the current version parsed from most recent git tag
        """
        # what to do on first time run? no tags yet..
        if self.current_tag:
            version = self.current_tag.lstrip('v')
        else:
            version = None

        if version and not version_is_valid(version):
            version = None

        return version

    @property
    def versions(self):
        """
        :returns: iterator of all valid versions parsed from the git tags
        """
        versions = (t.lstrip('v') for t in self.tags)
        return filter(version_is_valid, versions)

    def gen_versioned_files(self, wave):
        if self.file:
            yield self.file
        else:
            wave_one = [
                '*.spec', 'setup.cfg', 'setup.py', '*/__init__.py',
                '*.xml', '*.json']

            switch = {1: wave_one, 2: ['*.php', '*.py']}

            for git_file in self.files:
                if any(fnmatch(git_file, file) for file in switch[wave]):
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
                        cmd = ("sed -i '' '%ss/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s"
                            % (rep_line_num, new_version, file_))
                else:
                    cmd = None
            else:
                # replace current version with new version only if the line
                # contains the word 'version'
                cmd = ("sed -i '' '/version/s/%s/%s/g' %s"
                    % (self.version, new_version, file_))

            self.sh(cmd) if cmd else None

        self.bumped = self.is_dirty

    def ongeza(self, ongeza_type):
        """
        Parameters
        ----------
        version_num: string version name.
        ongeza_type: version ongeza type. one of:
            m = major - [x].0.0
            n = minor - x.[y].0
            p = patch - x.y.[z]

        Returns
        -------
        concatenated string of the incremented version name.
        """
        switch = {
            'm': semver.bump_major,
            'n': semver.bump_minor,
            'p': semver.bump_patch}

        new_version = switch.get(ongeza_type)(self.version)

        if new_version in set(self.versions):
            self.logger.error('version `%s` already present', new_version)
            new_version = None

        return new_version


def version_is_valid(version):
    try:
        return semver.parse(version)
    except (ValueError, TypeError):
        logger.debug('%s is not a valid version', version)
        return False
