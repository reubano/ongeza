"""
  keybump.package_utils
  ~~~~~~~~~~~~~~~~~~~~~

  helpers for working with the python package index.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from keybump.shell_utils import *


__all__ = ['set_version_in_file', 'set_init_py_version', 'set_setup_py_version',
'setup_py_distribute']


def set_version_in_file(filename, version_number, pattern):
  """
    :param filename:
    :param version_number:
    :param pattern:
  """
  changed = []

  def inject_version(match):
    before, old, after = match.groups()
    changed.append(True)
    return before + version_number + after

  with open(filename, "r") as f:
    data_str = re.sub(
      r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern, inject_version, f.read())
  if len(changed) < 1:
    fail(
      "could not set init file version. pattern {} not found in {}",
      pattern, filename)
  write(filename, data_str)


def set_init_py_version(version):
  """
    :param version:
  """
  info("setting __init__.py version to: {}", version)
  set_version_in_file("__init__.py", version, "__version__")


def set_setup_py_version(version):
  """
    :param version:
  """
  info("setting setup.py version to {}", version)
  set_version_in_file("setup.py", version, "version")


def setup_py_distribute():
  """
  uploads a dist build to the python package index.
  """
  sh("{} setup.py clean sdist upload", sys.executable)

