"""
  keybump.config
  ~~~~~~~~~~~~~~

  configuration for keybump projects.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from os import path
import yaml


__all__ = ['KeybumpConfig']


class KeybumpConfig(dict):
  """
  class representing a keybump configuration object.
  """

  DEFAULT_CONFIG_FILE = ".keybump.yaml"
  DEFAULT_SKIP_INTERACTIVE = False
  DEFAULT_SKIP_SET_INIT_PY_VERSION = False
  DEFAULT_SKIP_SET_SETUP_PY_VERSION = False
  DEFAULT_SKIP_TAG = False
  DEFAULT_SKIP_PUSH = False
  DEFAULT_SKIP_COMMIT = False
  DEFAULT_PYPI_DISTRIBUTE = True
  DEFAULT_CHANGELOG_FILE = "CHANGES.md"

  DEFAULT_TAG_MSG_FMT = "Version bumped to {version_num}"
  DEFAULT_COMMIT_MSG_FMT = "Version bumped to {version_num}"
  DEFAULT_SUMMARY_ITEM_PREFIX = "    * "
  DEFAULT_SUMMARY_SEPARATOR = "-"
  DEFAULT_DATESTR_FMT = "%Y-%m-%d"

  DEFAULT_CHANGELOG_FMT = """
  Version {version_num}
  ----------------------

  Released on {datestr}

{summaries}

  """

  @classmethod
  def from_cli_options(cls, options):
    rv = cls(
      bump_type=options.bump_type,
      skip_interactive=options.skip_interactive,
      skip_set_init_py_version=options.skip_set_init_py_version,
      skip_set_setup_py_version=options.skip_set_setup_py_version,
      skip_tag=options.skip_tag,
      skip_push=options.skip_push,
      skip_commit=options.skip_commit,
      pypi_distribute=options.pypi_distribute,
      changelog_file=options.changelog_file,
      changelog_fmt=options.changelog_fmt,
      commit_msg_fmt=options.commit_msg_fmt,
      summaryitem_fmt=options.summaryitem_fmt,
      tag_msg_fmt=options.tag_msg_fmt,
      datestr_fmt=options.datestr_fmt)

    if options.config_file:
      rv.load(options.config_file)

    return rv


  def __init__(self, *args, **kw):
    self.bump_type = None
    self.skip_interactive = self.DEFAULT_SKIP_INTERACTIVE
    self.skip_tag = self.DEFAULT_SKIP_TAG
    self.skip_push = self.DEFAULT_SKIP_PUSH
    self.skip_commit = self.DEFAULT_SKIP_COMMIT
    self.pypi_distribute = self.DEFAULT_PYPI_DISTRIBUTE
    self.changelog_file = self.DEFAULT_CHANGELOG_FILE
    self.changelog_fmt = self.DEFAULT_CHANGELOG_FMT
    self.summaryitem_fmt = self.DEFAULT_SUMMARY_ITEM_PREFIX
    self.commit_msg_fmt = self.DEFAULT_COMMIT_MSG_FMT
    self.tag_msg_fmt = self.DEFAULT_TAG_MSG_FMT
    self.datestr_fmt = self.DEFAULT_DATESTR_FMT
    self.summary_separator = self.DEFAULT_DATESTR_FMT
    dict.__init__(self, *args)
    if len(args) > 0:
      self.update(*args, **kw)
    else:
      self.update(None, **kw)



  def update(self, values, **kw):
    if values is None:
      values = {}

    if values:
      for k, v in values.iteritems():
        setattr(self, k, v)
    for k, v in kw.iteritems():
      setattr(self, k, v)
    return dict.update(self, values, **kw)


  def load(self, config_file):
    config_file = self.find_config_file(config_file)
    if config_file:
      self.update(yaml.load(config_file))


  def find_config_file(self, config_file):
    """
    searches the current working dir ./ and the home dir ~/ for '.keybump.yaml'
    """
    if config_file:
      if path.exists(config_file):
        return config_file
    else:

      # find a default configuration file either in the home dir or current
      # working dir..
      config_file = path.join(getcwd(), DEFAULT_CONFIG_FILE)
      if path.exists(config_file):
        return config_file

      else:
        config_file = path.expanduser("~/{}".format(DEFAULT_CONFIG_FILE))
        if path.exists(config_file):
          return config_file
