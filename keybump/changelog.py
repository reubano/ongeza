"""
  keybump.changelog
  ~~~~~~~~~~~~~~~~~

  base class for a keybump changelog.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from os import getcwd
from os import path
from keybump.shell_utils import *


__all__ = ['Changelog']


class Changelog(object):
  """
  class representing a changelog object.
  """

  def __init__(self, file_name, formatter=None, parser=None):
    self.path = self.find_file(file_name)
    self.formatter = formatter
    self.parser = parser

  def contents(self):
    return open(self.path, 'r').read()

  def open(self, mode="r"):
    return open(self.path, mode)

  def write(self, data):
    write(self.path, data)

  def prepend(self, data):
    contents = ""
    with self.open() as f:
      if isinstance(data, basestring):
        contents = data + "\n" + f.read()
      else:
        contents = f.readlines()
    write(self.path, contents)

  def format(self, version_num, datestr, summaryitem_fmt, summaries):
    return self.formatter.format(
      version_num=version_num,
      datestr=datestr,
      summaries=self.format_join(summaryitem_fmt, summaries))

  def format_join(self, fmt, items):
    return fmt + ("\n" + fmt).join(items)


  def find_file(self, file_name):
    """
    searches the current working dir ./ for CHANGES.md'
    """
    if file_name and path.exists(file_name):
        return file_name

    else:

      changelog_file = path.join(getcwd(), file_name)
      if path.exists(changelog_file):
        return changelog_file
