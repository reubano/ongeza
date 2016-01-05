# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab
"""
tests.test_main
~~~~~~~~~~~~~~~

Provides main unit tests.
"""
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import sys
import nose.tools as nt
import pygogo as gogo

from builtins import *

sys.path.append('../ongeza')
from ongeza import __version__ as version, TRAVIS
from ongeza.git_utils import Git
# from mock import patch

module_logger = gogo.Gogo(__name__).logger


def setup_module():
    """site initialization"""
    global initialized
    initialized = True
    print('Site Module Setup\n')


class TestGit:
    """Git unit tests"""
    cls_initialized = False

    def setUp(self):
        nt.assert_false(self.cls_initialized)
        self.cls_initialized = True
        self.git = Git()
        module_logger.debug('TestMain class setup\n')

    def tearDown(self):
        nt.ok_(self.cls_initialized)
        module_logger.debug('TestMain class teardown\n')

    def test_current_git_tag(self):
        tag = self.git.current_tag

        if not TRAVIS:
            nt.assert_equal(version, tag.lstrip('v'))

    def test_git_tags(self):
        tags = self.git.tags
        nt.assert_greater_equal(len(tags), 7)
        nt.assert_equal('v0.8.0', tags[0])

    # @patch('self.git.is_clean')
    # def test_normal(self, is_clean):
    #     """
    #     test that the script works with a clean index
    #     """
    #     is_clean.return_value = True
    #     nt.ok_(project.ongeza())

    # @patch('self.git.is_clean')
    # @patch('self.git.dirty_files')
    # def test_dirty(self, dirty_files, is_clean):
    #     """
    #     test that the script exits with dirty files
    #     """
    #     is_clean.return_value = False
    #     dirty_files.return_value = ['file1', 'file2']

    #     errmsg = 'aborting.. un[stashed/committed] changes'
    #     err = project.ongeza()
    #     nt.assert_in(errmsg, err)
    #     nt.assert_in('file1', err)
    #     nt.assert_in('file2', err)

    # @patch('self.git.stash')
    # @patch('self.git.is_clean')
    # @patch('self.git.dirty_files')
    # def test_stashing(self, dirty_files, is_clean, stash):
    #     """
    #     test that the script works by stashing dirty files
    #     """
    #     stash.return_value = None
    #     is_clean.return_value = False
    #     dirty_files.return_value = ['file1', 'file2']
    #     nt.ok_(project.ongeza())
