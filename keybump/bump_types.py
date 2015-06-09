"""
  keybump.bump_types
  ~~~~~~~~~~~~~~~~~~

  enum of bump types.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals


__all__ = ['MAJOR_BUMP', 'MINOR_BUMP', 'PATCH_BUMP', 'BUMP_TYPES']


MAJOR_BUMP = 'major'
MINOR_BUMP = 'minor'
PATCH_BUMP = 'patch'
BUMP_TYPES = [MAJOR_BUMP, MINOR_BUMP, PATCH_BUMP]
