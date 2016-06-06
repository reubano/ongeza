# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
ongeza.git_utils
~~~~~~~~~~~~~~~~

helpers for working with git.

Examples:
    basic usage::

        >>> Git().tags[:2] == ['v0.8.0', 'v0.8.1']
        True
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

from functools import partial, cmp_to_key

import semver
import pygogo as gogo

from builtins import *
from .shell_utils import sh

logger = gogo.Gogo(__name__, monolog=True).logger


class Git(object):
    """
    class representing Git commands.
    """
    def __init__(self, dir_=None, verbose=False):
        """
        Parameters
        ----------
        dir: directory containing the git project
        """
        self.dir = dir_
        self.stash_count = 0
        self.logger = logger
        self.sh = partial(sh, path=self.dir)

    @property
    def current_tag(self):
        """
            :returns: string of the current git tag on the git index, not the
            latest tag version created.
        """
        cmd = 'git describe --tags --abbrev=0'
        return self.sh(cmd, True)

    @property
    def is_clean(self):
        """
        Returns
        -------
        boolean if there is a dirty index.
        """
        return self.sh("git diff --quiet")

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
        files = self.sh("git diff --minimal --numstat", True)
        return [x.split("\t")[-1] for x in files.splitlines()]

    @property
    def files(self):
        """
        Returns
        -------
        list of string names of all files.
        """
        cmd = "git ls-tree --full-tree --name-only -r HEAD"
        return self.sh(cmd, True).splitlines()

    @property
    def tags(self):
        """
            :returns: list of git tags, sorted by the version number.
        """
        cmd = 'git tag'
        tags = self.sh(cmd, True).split('\n')
        compare = lambda x, y: semver.compare(x.lstrip('v'), y.lstrip('v'))
        return sorted(tags, key=cmp_to_key(compare))

    def add(self, files):
        files = ' '.join(files)
        self.logger.info('add files: "%s"', files)
        return self.sh('git add %s' % files)

    def commit(self, message):
        self.logger.info('making git commit: "%s"', message)
        return self.sh("git commit -m '%s'" % message)

    def tag(self, message, tag_text, sign=False):
        self.logger.info('making git tag: "%s"', message)
        opts = 'sm' if sign else 'm'
        cmd = "git tag -%s '%s' %s" % (opts, message, tag_text)
        return self.sh(cmd)

    def push(self):
        """
        pushes current branch and tags to remote.
        """
        return self.sh("git push && git push --tags")

    def stash(self):
        """
        stashes current changes in git.
        """
        if self.sh("git stash"):
            self.stash_count += 1

        return self.stash_count

    def unstash(self):
        """
        pops previous stash from git.
        """
        if self.stash_count and self.sh("git stash pop"):
            self.stash_count -= 1

        return self.stash_count
