"""
  keybump.project
  ~~~~~~~~~~~~~~~

  base class for a keybump project.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import re
from datetime import datetime
from logging import getLogger, DEBUG
from keybump import version
from keybump.changelog import Changelog
from keybump.release import Release
from keybump.git_utils import *
from keybump.shell_utils import *
from keybump.package_utils import *


__all__ = ['Project']


logger = getLogger(__name__)
logger.setLevel(DEBUG)


class Project(object):
  """
  base class representing a keybump configuration object.
  """

  @property
  def codename(self):
    if self.last_release:
      return self.last_release.codename

  @property
  def last_release(self):
    if self.release_count > 0:
      return self.releases[-1]

  @property
  def tags(self):
    if self._tags is None:
      self._tags = get_git_tags()
    return self._tags

  @property
  def has_initial_tag(self):
    return len(self.tags) > 0

  @property
  def release_count(self):
    return len(self.releases)

  def __init__(self, config=None):
    """
      :param config: instance of a KeybumpConfig object
    """
    self.config = config
    self.changelog = Changelog(config.changelog_file, config.changelog_fmt)

    # todo: don't copy these over.. ?
    self.skip_interactive = config.skip_interactive
    self.summaryformatter = None

    self.releases = []
    self._tags = None
    self.current_tag = None
    self.last_version_num = version.INITIAL_VERSION_NUM
    self.initial_version_summary_item = version.INITIAL_VERSION_SUMMARY_ITEM
    self.release_header_re = re.compile(
      "Released on (\d+-\d+-\d+)(?:, codename (.*))?(?i)")


  def parse_git_tags(self):
    """
    loads the repo's git tags, sets the `current_tag` + `latest_tag` attrs.
    """
    # what to do on first time run? no tags yet..
    if not self.has_initial_tag:
      fail("""
  looks as though the project has not been initialized yet for releases.

  create a tag for version: 0.0.0 and try again.

  sorry, we're still ghetto-riggin this script along.. workin on it..""")
      # todo: implement condition for new project without tags / version.
      # https://github.com/gregorynicholas/keybump/issues/2

    self.latest_tag = get_latest_git_tag()
    # logger.info 'get_latest_git_tag:', get_latest_git_tag()
    self.current_tag = self._current_or_last_git_tag()


  def _current_or_last_git_tag(self):
    """
    returns string name of the current or last git tag.
    """
    rv = get_current_git_tag()
    if rv not in self.tags:
      rv = self.latest_tag
    return rv


  def parse_versions(self):
    if not self.current_tag or len(self.current_tag) < 1:
      return
    non_decimal = re.compile(r"[^\d.]+")
    try:
      self.last_version_num = non_decimal.sub("", self.current_tag)
    except TypeError, e:
      logger.exception('TypeError: {} {}'.format(e, self.current_tag))
      raise e
    except Exception, e:
      logger.exception('ParseException: {}'.format(e))
      raise e


  def parse_releases(self):
    """
    sets the releases property, parsed from the changelog summaries.
    """
    self.releases = self.parse_changelog_to_releases()
    if len(self.releases) < 1:
      msg = "could not parse release from changelog history in {}.".format(
        self.changelog.path)

      # fail and exit..
      if self.config.skip_interactive:
        fail(msg)
      else:
        # don't fail, set to initial version..
        info(msg)

      self.setup_initial_release()


  def parse_changelog_to_releases(self):
    """
    parses the contents of the changelog file, and returns a list of `Release`
    objects from the changelog summary.

      :returns: list of instance of a `Release` objects.
    """
    result = []

    # todo: need to handle encoding..
    with self.changelog.open() as f:
      lineiter = iter(f)
      hasdata = False
      version_num = None

      for line in lineiter:
        logger.debug('line: {}'.format(line))
        hasdata = True

        # parse the last version..
        ver_match = version.VERSION_RE.search(line.strip())
        if ver_match is None:
          logger.warn('continuing..!')
          continue

        version_num = ver_match.group(1).strip()
        # logger.debug('version_num: {}'.format(version_num))

        value = lineiter.next()
        # logger.debug('value: {}'.format(value))

        if not value.count(self.config.summary_separator):
          # TODO: this is currently breaking things..
          # logger.warn('continuing..!')
          # continue
          pass

        # parse the release data and codename..
        while 1:
          release_header = lineiter.next().strip()
          if release_header:
            logger.debug('release_header: {}'.format(release_header))
            break

        rel_match = self.release_header_re.search(release_header)
        if rel_match is None:
          # TODO: raise exception here?
          logger.warn('no release header found!')
          # continue

        datestr, codename = rel_match.groups()
        logger.debug('datestr: {}'.format(datestr))

        # parse the change summary messages..
        summaries = []
        while 1:
          try:
            summary = lineiter.next()
          except StopIteration, e:
            break
          if summary:
            if len(summary.strip()) > 0:
              # strip summary_item_fmt front beginning of item..
              total = len(self.config.summaryitem_fmt)
              if summary[0:total] == self.config.summaryitem_fmt:
                summary = summary[total:]
              # remove newline char at end..
              summaries.append(summary[:-1])
          else:
            break

        release = Release(
          self, version_num, datestr=datestr, summaries=summaries)
        logger.debug('release: {}'.format(release))
        logger.debug('summaries: {}'.format(summaries))

        result.append(release)

      if len(result) == 0 and hasdata:
        fail("""unable to parse the changelog contents.

        format not recognized by parser:

        {}""".format(self.changelog.contents()))
      return result


  def setup_initial_release(self):
    """
    """
    if not choice("""
  do you want keybump to setup the initial release?"""):
      fail('aborting, initial release not created.')

    info("""
  ok, you asked for it..
    """)
    release = self.create_initial_release()
    self.changelog.write(release.format_changelog_summary())
    self.releases.append(release)

    # TODO create initial tag


  def create_initial_release(self, version_num=version.INITIAL_VERSION_NUM):
    """
    creates a default initial release of 0.0.0
    """
    return Release(
      self,
      version_num,
      datestr=self.today_str(),
      summaries=[self.initial_version_summary_item])


  def new_release(self):
    """
      :returns: instance of a `Release` object.
    """
    rv = Release(self, self.last_release.version_num, datestr=self.today_str())
    rv.bump()

    if rv.version_num in self.tags:
      fail("version `{}` is already tagged", rv.version_num)

    rv.set_summaries(
      self.get_changelog_summaries_since(self.current_tag))
    return rv


  def get_changelog_summaries_since(self, latest_tag):
    """
      :param latest_tag:
      :returns: string list of git commit messages between the `latest_tag`
        and the latest commit
    """
    sep = "__||__"
    rv = sh("git log --no-merges --pretty=%B{} {}..", sep, latest_tag)
    return [x.strip() for x in rv.split(sep)]


  def today_str(self):
    return datetime.now().strftime(self.config.datestr_fmt)


  def __str__(self):
    INFO_FMT = """project version information:

  latest tag:   {}
  current tag:  {}
  version id:   {}"""

    return INFO_FMT.format(
      self.latest_tag, self.current_tag, self.last_version_num)
