"""
    tests.testcase
    ~~~~~~~~~~~~~~

    :copyright: (c) 2015 by gregorynicholas.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals

from unittest import TestCase
from mock import patch, MagicMock
from StringIO import StringIO


__all__ = ['KeybumpTestCase']


class KeybumpTestCase(TestCase):
    """
    base class for keybump tests.
    """

    def __call__(self, result=None):
        """
        performing setup here means subclasses don't have to call `super.setUp()`
        """
        try:
            self._pre_setup()
            TestCase.__call__(self, result)
        finally:
            self._post_teardown()

    def _pre_setup(self):
        # monkey patch keybump's stdout + stdin..
        self.stdout = StringIO()
        self.stdout_patcher = patch("keybump.shell_utils.stdout")
        self.stdout_patcher.start().return_value = self.stdout

        self.stderr = StringIO()
        self.stderr_patcher = patch("keybump.shell_utils.stderr")
        self.stderr_patcher.start().return_value = self.stderr

    def _post_teardown(self):
        self.stdout_patcher.stop()
        self.stderr_patcher.stop()
