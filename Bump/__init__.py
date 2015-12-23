# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
bump
~~~~

An automated way to follow the Semantic Versioning Specification

Examples:
    basic usage::

        >>> from os import path as p
        >>> project = Project(p.abspath(p.dirname(p.dirname(__file__))))
        >>> project.current_version  == __version__
        True

Attributes:
    DEFAULT_TAG_FMT (str): The default tag format
    DEFAULT_TAG_MSG_FMT (str): The default tag message format
    DEFAULT_COMMIT_MSG_FMT (str): The default commit message format
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import os
import semver

from fnmatch import fnmatch
from subprocess import CalledProcessError

from .git_utils import Git
from .shell_utils import sh

__version__ = '1.3.0'

__title__ = 'bump'
__author__ = 'Reuben Cummings'
__description__ = 'An automated way to follow the Semantic Versioning'
__description__ += 'Specification'
__email__ = 'reubano@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Reuben Cummings'

DEFAULT_TAG_FMT = 'v{version}'
DEFAULT_TAG_MSG_FMT = 'Version {version} Release'
DEFAULT_COMMIT_MSG_FMT = 'bump to version {version}'


class Project(Git):
    """
    class representing a project object.
    """

    def __init__(self, dir_, file_=None, version=None, verbose=False):
        """
        Parameters
        ----------
        dir : str
            the project directory

        file_ : str
            the file to search for a version

        Examples
        --------
        >>> Project(os.curdir)  # doctest: +ELLIPSIS
        <bump.Project object at 0x...>
        """
        if not os.path.isdir(dir_):
            raise Exception('%s is not a directory' % dir_)

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
        :returns: string of the current git tag on the git index, not the
        latest tag version created.
        """
        # what to do on first time run? no tags yet..
        if self.current_tag:
            version = self.current_tag.lstrip('v')
        else:
            version = None

        if version and not self.version_is_valid(version):
            version = None

        return version

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

    def set_versions(self, new_version, version, wave=1):
        for file_ in self.gen_versioned_files(wave):
            if not version:
                # get all lines in file
                cmd = 'grep -ine "" %s' % file_

                try:
                    lines = sh(cmd, True, path=self.dir)
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
                        rep_line = sh(cmd, True, path=self.dir)
                    except Exception:
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
                    % (version, new_version, file_))

            sh(cmd, path=self.dir) if cmd else None

        self.bumped = self.is_dirty

    def version_is_valid(self, version):
        try:
            return semver.parse(version)
        except ValueError as err:
            self.logger.error(err.message)
            return False

    def bump(self, bump_type):
        """
        Parameters
        ----------
        version_num: string version name.
        bump_type: version bump type. one of:
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

        new_version = switch.get(bump_type)(self.version)

        if new_version in self.version:
            self.logger.error('version `%s` already present', new_version)
        else:
            self.version = new_version
            return self.version
