"""
  keybump.release
  ~~~~~~~~~~~~~~~

  base class for a keybump release.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import re
from datetime import datetime
from keybump import version
from keybump.bump_types import *
from keybump.shell_utils import *


__all__ = ['Release']


class Release(object):
  """
  base class representing a release object.
  """

  def __init__(self, project, version_num, datestr=None, summaries=None):
    """
      :param version_num: string version in the format: [x].[x].[x]
    """
    self.project = project
    self.version_num = version_num or version.INITIAL_VERSION_NUM
    self.set_date(datestr)
    self.set_summaries(summaries or [])
    self.codename = project.codename


  @property
  def tag_msg(self):
    return self.project.config.tag_msg_fmt.format(self.version_num)

  @property
  def commit_msg(self):
    return self.project.config.commit_msg_fmt.format(
      version_num=self.version_num,
      datestr=self.datestr)

  @property
  def datestr(self):
    return self.date.strftime(self.project.config.datestr_fmt)


  def set_date(self, datestr=None):
    """
      :param datestr: string date in the format: %Y-%m-%d. defaults to today.
    """
    self.date = self._parse_datestr(datestr or self.project.today_str())


  def _parse_datestr(self, datestr):
    """
      :param datestr: string date in the format: %Y-%m-%d
      :returns: `datetime.date` object parsed from the `datestr` param
    """
    date_clean_re = re.compile(r"(\d+)(st|nd|rd|th)")
    datestr = date_clean_re.sub(r"\1", datestr)
    return datetime.strptime(datestr, self.project.config.datestr_fmt)


  def set_summaries(self, summaries):
    """
      :param summaries:
    """
    self.summaries = self._format_summary_items(summaries)


  def _format_summary_items(self, summaries):
    """
    cleans summary lines of text. removes 'merge branch' commit messages.

      :param summaries:
      :returns:
    """
    MIN_SUMMARY_LENGTH = 10
    SKIP_PREFIXES = ["MERGE BRANCH", "MERGE PULL REQUEST"]
    SKIP_EQUALITY = ["WHITESPACE"]
    rv = []
    for line in summaries:
      # merge commits..
      lineUpper = line.upper()
      for skip in SKIP_PREFIXES:
        if lineUpper.startswith(skip):
          continue
      for skip in SKIP_EQUALITY:
        if lineUpper == skip:
          continue
      if len(lineUpper) < MIN_SUMMARY_LENGTH:
        continue
      rv.append(line)
    return rv


  def format_changelog_summary(self):
    """
      :returns: formatted string of the release changelog summary.
    """
    return self.project.changelog.format(
      version_num=self.version_num,
      datestr=self.datestr,
      summaryitem_fmt=self.project.config.summaryitem_fmt,
      summaries=self.summaries)


  def _bump_num(self, version_num, bump_type=PATCH_BUMP):
    """
      :param version_num: string version name.
      :param bump_type: version bump type. one of:
          major  [x].0.0    minor  x.[x].0    patch  x.x.[x]
      :returns: concatenated string of the incremented version name.
    """
    # split the version number into a list of ints..
    try:
      version = [int(v) for v in version_num.split(".")]
      switch = {
        "major": lambda: [version[0] + 1, 0, 0],
        "minor": lambda: [version[0], version[1] + 1, 0],
        "patch": lambda: [version[0], version[1], version[2] + 1]}
      return ".".join(map(str, switch.get(bump_type)()))
    except ValueError:
      fail("version string: {} is an invalid format..", version_num)


  def bump(self, bump_type=PATCH_BUMP):
    """
      :param bump_type: version bump type. one of:
          major  [x].0.0    minor  x.[x].0    patch  x.x.[x]
    """
    self.version_num = self._bump_num(self.version_num, bump_type)


  def __str__(self):
    rv = ""
    if self.project.last_release is not None:
      rv +=  """
  previous release: {} (codename: {}, date: {})
      """.format(
        self.project.last_release.version_num, self.project.codename,
        self.project.last_release.date)

    rv += """
  creating release: {} (codename: {}, date: {})
  """.format(
      self.version_num, self.codename, self.date)

    return rv
