#!/usr/bin/env python
"""
  keybump_tests
  ~~~~~~~~~~~~~

  :copyright: (c) 2013 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
import os
import unittest
import tempfile
from mock import patch, MagicMock
from StringIO import StringIO


def monkey_keybump_module():
  """
  monkeypatch the script as a python module..
  """
  import shutil
  unmonkey_keybump_module()
  shutil.copy("keybump", "keybump.py")


def unmonkey_keybump_module():
  """
  undo the keybump module monkeypatch..
  """
  if os.path.exists("keybump.py"):
    os.remove("keybump.py")
  if os.path.exists("keybump.pyc"):
    os.remove("keybump.pyc")

monkey_keybump_module()
import keybump


class TestCase(unittest.TestCase):
  def __call__(self, result=None):
    """
    doing setup here means subclasses don't have to call super.setUp.
    """
    try:
      self._pre_setup()
      unittest.TestCase.__call__(self, result)
    finally:
      self._post_teardown()

  def _pre_setup(self):
    # monkey patch keybump's stdout + stdin..
    self.stdout = StringIO()
    self.stdout_patcher = patch("keybump.stdout")
    self.stdout_patcher.start().return_value = self.stdout

    self.stderr = StringIO()
    self.stderr_patcher = patch("keybump.stderr")
    self.stderr_patcher.start().return_value = self.stderr

  def _post_teardown(self):
    self.stdout_patcher.stop()
    self.stderr_patcher.stop()


class GitHelperTests(TestCase):

  @patch("keybump.sh")
  def test_get_current_git_tag(self, sh):
    sh.return_value = "abcd1234"
    rv = keybump.get_current_git_tag()
    self.assertIsNotNone(rv)
    self.assertEquals(rv, "abcd1234")

  def test_sh(self):
    rv = keybump.sh("git describe")
    self.assertIsInstance(rv, basestring)

  @patch("keybump.sh")
  def test_get_git_tags(self, sh):
    sh.return_value = """0.0.0
0.0.1"""
    rv = keybump.get_git_tags()
    self.assertIsNotNone(rv)
    self.assertIsInstance(rv, list)
    self.assertEquals(2, len(rv))
    self.assertEquals(rv[0], "0.0.0")
    self.assertEquals(rv[1], "0.0.1")

  @patch("keybump.git_is_clean")
  def test_ensure_clean_index_valid_returns(self, git_is_clean):
    """
    test the return value is `True` when the git index is clean
    """
    git_is_clean.return_value = True
    rv = keybump.ensure_clean_index()
    self.assertEquals(True, rv)

  @patch("keybump.git_is_clean")
  @patch("keybump.git_diff_files")
  @patch("keybump.stderr")
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
      keybump.ensure_clean_index(skip_interactive=True)

    errmsg = "cannot bump the version with a dirty git index."
    errv = self.stderr.getvalue()
    self.assertIn(errmsg, errv)
    self.assertIn("file1", errv)
    self.assertIn("file2", errv)

  @patch("keybump.git_stash")
  @patch("keybump.git_is_clean")
  @patch("keybump.git_diff_files")
  @patch("keybump.input")
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
    rv = keybump.ensure_clean_index(False, callback)
    self.assertEquals(True, rv)

    msg = "ok, you asked for it.."
    outv = self.stdout.getvalue()
    self.assertTrue(msg in outv)
    callback.assert_called()

  @patch("keybump.git_stash")
  @patch("keybump.git_is_clean")
  @patch("keybump.git_diff_files")
  @patch("keybump.input")
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
      keybump.ensure_clean_index(False)

    errmsg = "not continuing due to dirty index, fix that shit"
    self.assertIn(errmsg, self.stderr.getvalue())


class ProjectClassTests(TestCase):
  def setUp(self):
    self.changelogfs, self.changelog = tempfile.mkstemp(
      prefix="changes-", suffix=".md")
    self.project = keybump.Project(self.changelog, skip_interactive=False)

  def test_class_instantiation(self):
    rv = keybump.Project(self.changelog, skip_interactive=False)
    self.assertIsNotNone(rv)
    self.assertEquals(rv.last_version_num, "0.0.0")

  @patch("keybump.input")
  def test_no_changelog_releases_prompts_initial_fails(self, input):
    """
    test that when no changelog releases are parsed, the initial setup
    is prompted and then fails.
    """
    input.return_value = "N"
    with self.assertRaises(SystemExit):
      self.project.parse_releases()

  @patch("keybump.input")
  def test_no_changelog_releases_sets_initial_release_success(self, input):
    """
    test that when no changelog releases are parsed, the initial setup
    is prompted, and then succeeds.
    """
    input.return_value = "Y"
    self.project.parse_releases()
    self.assertEquals(1, len(self.project.releases))
    rel = self.project.releases[0]
    self.assertEquals(rel, self.project.last_release)
    self.assertEquals("0.0.0", rel.version_num)
    self.assertEquals(1, len(rel.summaries))
    summary = rel.summaries[0]
    self.assertEquals("initial version setup", summary)

  def test_parse_changelog_to_releases_fails(self):
    pass

  def test_parse_changelog_to_releases_success(self):
    pass

  def test_new_release_success(self):
    pass

  def test_parse_versions_success(self):
    pass


class ReleaseClassTests(TestCase):
  def setUp(self):
    pass


class SummaryFormatterTests(TestCase):
  pass


class KeybumpTests(TestCase):
  pass


if __name__ == "__main__":
  unittest.main(exit=False)
  unmonkey_keybump_module()
