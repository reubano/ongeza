"""
  keybump.formatter
  ~~~~~~~~~~~~~~~~~

  base class for a commit summary formatter.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from keybump.shell_utils import *


__all__ = ['BaseSummaryFormatter']


class BaseSummaryFormatter(object):
  """
  base class for a commit summary formatter.
  """

  def __init__(self, format):
    self.format = format


class SummaryFormatter(BaseSummaryFormatter):
  """
  commit summary formatter.
  """

  def __init__(self, *args):
    BaseSummaryFormatter.__init__(self, *args)
