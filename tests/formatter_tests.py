#!/usr/bin/env python
"""
  tests.formatter_tests
  ~~~~~~~~~~~~~~~~~~~~~

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import unittest
from mock import patch, MagicMock
from tests.testcase import KeybumpTestCase

import keybump
from keybump import version
from keybump.config import KeybumpConfig
from keybump.project import Project


class SummaryFormatterTests(KeybumpTestCase):
  pass


if __name__ == "__main__":
  unittest.main(exit=False)
