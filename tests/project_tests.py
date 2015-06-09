#!/usr/bin/env python
"""
  tests.project_tests
  ~~~~~~~~~~~~~~~~~~~

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import unittest
import tempfile
from mock import patch, MagicMock
from tests.testcase import KeybumpTestCase

import keybump
from keybump import version
from keybump.config import KeybumpConfig
from keybump.project import Project


class ProjectTests(KeybumpTestCase):
  def setUp(self):
    _, self.changelog = tempfile.mkstemp(
      prefix="changes-", suffix=".md")

    config = KeybumpConfig({
      "changelog_file": self.changelog,
      "skip_interactive": False
    })

    self.project = Project(config)


  def test_class_instantiation(self):
    config = KeybumpConfig({
      "changelog_file": self.changelog,
      "skip_interactive": False
    })
    rv = Project(config)
    self.assertIsNotNone(rv)
    self.assertEquals(rv.last_version_num, version.INITIAL_VERSION_NUM)


  @patch("keybump.shell_utils.input")
  def test_no_changelog_releases_prompts_initial_fails(self, input):
    """
    test that when no changelog releases are parsed, the initial setup
    is prompted and then fails.
    """
    input.return_value = "N"
    with self.assertRaises(SystemExit):
      self.project.parse_releases()


  @patch("keybump.shell_utils.input")
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
    self.assertEquals(version.INITIAL_VERSION_NUM, rel.version_num)
    self.assertEquals(1, len(rel.summaries))

    summary = rel.summaries[0]
    self.assertEquals("initial version setup", summary)


  @patch("keybump.shell_utils.input")
  def test_parse_changelog_with_invalid_contents_fails(self, input):
    input.return_value = "Y"
    with open(self.changelog, "w") as f:
      f.write("something random")

    with self.assertRaises(SystemExit):
      self.project.parse_releases()

    errmsg = "unable to parse the changelog contents"
    self.assertIn(errmsg, self.stderr.getvalue())


  def test_parse_changelog_to_releases_success(self):
    """
    test that valid changelog contents does not prompt for interactive input,
    and parses to `Release` objects properly.
    """
    datestr = self.project.today_str()
    summs = ["testing some shit", "testing another item"]

    with open(self.changelog, "w") as f:
      contents = self.project.changelog.format(
        version_num="0.0.0",
        datestr=datestr,
        summaryitem_fmt=self.project.config.summaryitem_fmt,
        summaries=summs)
      f.write(contents)

    self.project.parse_releases()

    self.assertEquals(1, self.project.release_count)

    self.assertEquals("0.0.0", self.project.last_release.version_num)

    self.assertEquals(datestr, self.project.last_release.datestr)

    self.assertEquals(
      summs[0], self.project.last_release.summaries[0])

    self.assertEquals(
      summs[1], self.project.last_release.summaries[1])


if __name__ == "__main__":
  unittest.main(exit=False)
