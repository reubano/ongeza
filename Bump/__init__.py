#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

bump
----

An automated way to follow the Semantic Versioning Specification

"""

__title__ = 'bump'
__package_name__ = 'bump'
__author__ = 'Reuben Cummings'
__description__ = 'An automated way to follow the Semantic Versioning '
__description__ += 'Specification'
__email__ = 'reubano@gmail.com'
__version__ = '1.1.0'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Reuben Cummings'

import os
import semver

from fnmatch import fnmatch
from subprocess import call, check_output, CalledProcessError


def sh(cmd, output=False):
    if output:
        return check_output(cmd, shell=True)
    else:
        return call(cmd, shell=True) is 0


class Project(object):
    """
    class representing a project object.
    """

    def __init__(self, dir_, file_=None, version=None):
        """
        Parameters
        ----------
        dir : str
            the project directory

        file_ : str
            the file to search for a version

        Examples
        --------
        >>> Project(os.curdir)  #doctest: +ELLIPSIS
        <Bump.Project object at 0x...>
        """
        self.dir = dir_

        if not os.path.isdir(self.dir):
            raise Exception('%s is not a directory' % (self.dir))

        self.current_tag = None
        self.bumped = False
        self.file = file_

        if version:
            self.version = version
        else:
            cmd = 'cd %s; git describe --tags --abbrev=0' % (self.dir)
            self.version = sh(cmd, True).lstrip('v').rstrip()

        self.has_tag = sh('cd %s; git tag' % (self.dir), True)

    @property
    def is_clean(self):
        """
        Returns
        -------
        boolean if there is a dirty index.
        """
        return sh("cd %s; git diff --quiet" % self.dir)

    @property
    def is_dirty(self):
        """
        Returns
        -------
        boolean if there is a dirty index.
        """
        return not self.is_clean

    @property
    def dirty_files(self):
        """
        Returns
        -------
        list of string names of the dirty files.
        """
        files = sh("cd %s; git diff --minimal --numstat" % self.dir, True)
        return [x.split("\t")[-1] for x in files.splitlines()]

    def gen_versioned_files(self):
        if (self.file):
            yield self.file
        else:
            cmd = "git ls-tree --full-tree --name-only -r HEAD"
            git_files = sh(cmd, True).splitlines()
            no_matches = True

            wave_one = [
                '*.spec', 'setup.cfg', 'setup.py', '*/__init__.py',
                '*.xml', '*.json']

            for git_file in git_files:
                if any(fnmatch(git_file, file) for file in wave_one):
                    yield git_file
                    no_matches = False

            if no_matches:
                wave_two = ['*.php', '*.py']

                for git_file in git_files:
                    if any(fnmatch(git_file, file) for file in wave_two):
                        yield git_file

    def set_versions(self, new_version, version):
        for file_ in self.gen_versioned_files():
            if not version:
                # get all lines in file
                cmd = 'cd %s; grep -ine "" %s' % (self.dir, file_)

                try:
                    lines = sh(cmd, True)
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
                        rep_line = sh(cmd, True)
                    except Exception:
                        cmd = None
                    else:
                        rep_line_num = rep_line.split(':')[0]
                        # replace with new version number
                        sh("cd %s" % self.dir)
                        cmd = ("sed -i '' '%ss/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s"
                            % (rep_line_num, new_version, file_))
                else:
                    cmd = None
            else:
                # replace current version with new version only if the line
                # contains the word 'version'
                cmd = ("cd %s; sed -i '' '/version/s/%s/%s/g' %s"
                    % (self.dir, version, new_version, file_))

            sh(cmd) if cmd else None

        self.bumped = self.is_dirty

    def check_version(self, new_version):
        cmd = ("echo %s | sed 's/[0-9]*\.[0-9]*\.[0-9]*/@/g'"
            % new_version)
        return sh(cmd, True).splitlines()[0] is '@'

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

        return switch.get(bump_type)(self.version)


class Git(object):
    """
    class representing Git commands.
    """
    def __init__(self, dir):
        """
        Parameters
        ----------
        dir: directory containing the git project
        """
        self.dir = dir

    def add(self, files):
        files = ' '.join(files)
        return sh('cd %s; git add %s' % (self.dir, files))

    def commit(self, message):
        return sh("cd %s; git commit -m '%s'" % (self.dir, message))

    def tag(self, message, version):
        cmd = "cd %s; git tag -sm '%s' v%s" % (self.dir, message, version)
        return sh(cmd)

    def push(self):
        """
        pushes current branch and tags to remote.
        """
        # don't call --all here on purpose..
        return sh("cd %s; git push && git push --tags" % self.dir)
