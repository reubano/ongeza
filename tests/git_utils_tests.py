#!/usr/bin/env python
"""
    tests.git_utils_tests
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by gregorynicholas.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import unittest
from mock import patch, MagicMock
from tests.testcase import KeybumpTestCase
import keybump


class GitUtilsTests(KeybumpTestCase):

    def test_get_current_git_tag(self):
        expected = "3.0.1"

        tag = keybump.git_utils.get_current_git_tag()

        self.assertIsNotNone(tag)
        self.assertEquals(expected, tag,
            "get_current_git_tag should have returned '{}' not: '{}'".format(expected, tag))


    def test_sh_shell_methods(self):
        describe = keybump.shell_utils.sh("git describe")
        self.assertIsInstance(describe, basestring)

        describe = keybump.shell_utils.shell("git describe").output()[0]
        self.assertIsInstance(describe, basestring)

        if '-' in describe:
            describe = describe.split('-')[0]

        self.assertTrue(describe == '3.0.1')


    def test_get_git_tags(self):
        tags = keybump.git_utils.get_git_tags()
        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)

        self.assertEquals(3, len(tags),
            'there should be 3 git tags: {} count: {}'.format(tags, len(tags)))

        tag1, tag2, tag3 = tags

        self.assertEquals("2.0.1", tag1)
        self.assertEquals("3.0.0", tag2)
        self.assertEquals("3.0.1", tag3)


    @patch("keybump.git_utils.has_unstaged_changes")
    @patch("keybump.git_utils.has_uncommitted_changes")
    @patch("keybump.git_utils.git_is_clean")
    def test_ensure_clean_index_valid_returns(self, git_is_clean, has_uncommitted_changes, has_unstaged_changes):
        """
        test the return value is `True` when the git index is clean
        """
        has_unstaged_changes.return_value = False
        has_uncommitted_changes.return_value = False
        git_is_clean.return_value = True

        # TODO
        rv = keybump.git_utils.ensure_clean_index(skip_interactive=True)
        self.assertTrue(rv)


    @patch("keybump.git_utils.git_is_clean")
    @patch("keybump.git_utils.git_diff_files")
    @patch("keybump.shell_utils.stderr")
    def test_ensure_clean_index_invalid_fails(
        self, stderr, git_diff_files, git_is_clean):
        """
        test that the script exits with dirty index when skipping the
        interactive cli
        """
        stderr.return_value = self.stderr
        git_diff_files.return_value = ["file1", "file2"]
        git_is_clean.return_value = False

        with self.assertRaises(SystemExit):
            keybump.git_utils.ensure_clean_index(skip_interactive=True)

        error_msg = "aborting.. un[stashed/committed] changes"
        err = self.stderr.getvalue()
        self.assertIn(error_msg, err)

        self.assertIn("file1", err)
        self.assertIn("file2", err)


    @patch("keybump.git_utils.git_stash")
    @patch("keybump.git_utils.git_is_clean")
    @patch("keybump.git_utils.git_diff_files")
    @patch("keybump.shell_utils.input")
    def test_ensure_clean_index_invalid_interactive_works(
        self, input, git_diff_files, git_is_clean, git_stash):
        """
        test that when the interactive input returns "Y", the function invokes
        the recursive callback and returns `True`
        """
        git_stash.return_value = None
        git_is_clean.return_value = False
        git_diff_files.return_value = ["file1", "file2"]
        input.return_value = "Y"

        callback = MagicMock(return_value=True)
        rv = keybump.git_utils.ensure_clean_index(False, callback)
        self.assertEquals(True, rv)

        msg = "ok, you asked for it.."
        outv = self.stdout.getvalue()
        self.assertTrue(msg in outv)
        callback.assert_called()


    @patch("keybump.git_utils.git_stash")
    @patch("keybump.git_utils.git_is_clean")
    @patch("keybump.git_utils.git_diff_files")
    @patch("keybump.shell_utils.input")
    def test_ensure_clean_index_invalid_interactive_fails(
        self, input, git_diff_files, git_is_clean, git_stash):
        """
        test that the script exits when the interactive input does not
        return "Y"
        """
        git_stash.return_value = None
        git_is_clean.return_value = False
        git_diff_files.return_value = ["file1", "file2"]
        input.return_value = "N"

        with self.assertRaises(SystemExit):
            keybump.git_utils.ensure_clean_index(False)

        errmsg = "aborting.. un[stashed/committed] changes"
        self.assertIn(errmsg, self.stderr.getvalue())


if __name__ == "__main__":
    unittest.main(exit=False)
