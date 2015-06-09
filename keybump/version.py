"""
  keybump.version
  ~~~~~~~~~~~~~~~

  helpers for versions.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import re


__all__ = ['INITIAL_VERSION_NUM', 'INITIAL_VERSION_SUMMARY_ITEM', 'VERSION_RE']


INITIAL_VERSION_NUM = "0.0.0"
INITIAL_VERSION_SUMMARY_ITEM = "initial version setup"
VERSION_RE = re.compile("^Version\s+(.*)")
