#!/Users/gregorynicholas/.virtualenvs/gae_rp_local/bin/python
"""
  keybump
  ~~~~~~~~~~~~~~~~~~~

  Helper script to perform a project release, and follow the Semantic Versioning
  Specification.

  :copyright: (c) 2012 by gregorynicholas.
  :license: BSD, see LICENSE for more details.
"""
import re
import sys
from sys import exit
from argparse import RawTextHelpFormatter
from argparse import ArgumentParser
from datetime import datetime
from subprocess import Popen, PIPE


CHANGELOG = 'CHANGES.md'
SEP = '-'

MAJOR_BUMP = 'm'
MINOR_BUMP = 'n'
PATCH_BUMP = 'p'


_date_clean_re = re.compile(r'(\d+)(st|nd|rd|th)')


def fail(message, *args):
  print >> sys.stderr, 'Error:', message % args
  exit(1)

def info(message, *args):
  print >> sys.stdout, message % args
  # print >> sys.stderr, message % args

def _call(*args, **kwargs):
  return Popen(args, **kwargs).wait()


def bump_changelog(version):
  '''
  '''
  _call('git-changelog', CHANGELOG, version)

def parse_changelog(last_tag, last_version):
  '''
    :returns:
  '''
  with open(CHANGELOG) as f:
    lineiter = iter(f)
    for line in lineiter:
      # find the latest version header..
      match = re.search('^Version\s+(.*)', line.strip())
      if match is None:
        continue
      version = match.group(1).strip()
      value = lineiter.next()
      if not value.count(SEP):
        continue
      # parse the release data and codename..
      while 1:
        change_info = lineiter.next().strip()
        if change_info:
          break
      match = re.search(r'Released on (\d+-\d+-\d+)'
      # match = re.search(r'Released on (\w+\s+\d+\w+\s+\d+)'
        r'(?:, codename (.*))?(?i)', change_info)
      if match is None:
        continue
      datestr, codename = match.groups()
      info('datestr: %s', datestr)
      # parse the change summary messages..
      summaries = []
      while 1:
        summary = lineiter.next().strip()
        if summary:
          summaries.append(summary)
        else:
          break
      # clean up summaries..
      for line in summaries:
        if line.startswith('Merge branch '):
          summaries.remove(line)
        elif line == 'whitespace.':
          summaries.remove(line)
        elif len(line) < 10:
          summaries.remove(line)
      return version, parse_date(datestr), codename, summaries


def bump_version_num(version, bump_type=PATCH_BUMP):
  '''
    :param version:
    :param bump_type: Version bump type. Can be one of:
      MAJOR_BUMP    'm' = major (x.0.0)
      MINOR_BUMP    'n' = minor (1.y.0)
      PATCH_BUMP    'p' = patch (1.0.z)
    :returns:
  '''
  try:
    switch = {
      'm': lambda: [version[0] + 1, 0, 0],
      'n': lambda: [version[0], version[1] + 1, 0],
      'p': lambda: [version[0], version[1], version[2] + 1]}
    return '.'.join(map(str, switch.get(bump_type)()))
  except ValueError:
    fail('Current version is not numeric..')


def parse_date(string):
  '''
    :param string:
    :returns:
  '''
  string = _date_clean_re.sub(r'\1', string)
  # return datetime.strptime(string, '%B %d %Y')
  return datetime.strptime(string, '%Y-%m-%d')


def set_filename_version(filename, version_number, pattern):
  '''
    :param filename:
    :param version_number:
    :param pattern:
  '''
  changed = []
  def inject_version(match):
    before, old, after = match.groups()
    changed.append(True)
    return before + version_number + after
  with open(filename) as f:
    contents = re.sub(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern,
      inject_version, f.read())
  if not changed:
    fail('Could not find %s in %s', pattern, filename)
  with open(filename, 'w') as f:
    f.write(contents)

def set_init_version(version):
  '''
    :param version:
  '''
  info('Setting __init__.py version to %s', version)
  set_filename_version('__init__.py', version, '__version__')

def set_setup_version(version):
  '''
    :param version:
  '''
  info('Setting setup.py version to %s', version)
  set_filename_version('setup.py', version, 'version')

def build_and_upload():
  '''
  '''
  _call(sys.executable, 'setup.py', 'sdist', 'upload')


def get_git_tag():
  tag, err = Popen(['git', 'describe'], stdout=PIPE).communicate()
  return tag

def get_git_tags():
  cmd = "git for-each-ref --sort='*authordate' --format='%(tag)' refs/tags".split(' ')
  tags, err = Popen(cmd, stdout=PIPE).communicate()
  return tags.splitlines()

def has_git_tag(tags):
  '''
  check if repo has any git tags.

    :param tags:
  '''
  return tags and len(tags) > 0

def git_is_clean():
  '''
  '''
  return _call('git', 'diff', '--quiet') == 0

def git_checkout(id):
  '''
  '''
  info('Checking out: "%s"', id)
  return _call('git', 'checkout', id)

def make_git_commit(message):
  '''
    :param message:
  '''
  info('Making commit: "%s"', message)
  _call('git', 'add', CHANGELOG)
  _call('git', 'commit', '-am', message)

def make_git_tag(msg, tag_name):
  '''
    :param tag_name:
  '''
  info('Making tag: "%s"', tag_name)
  _call('git', 'tag', tag_name, '-m', msg)
  _call('git', 'push')
  _call('git', 'push', '--tags')


parser = ArgumentParser(
  description="description: bump makes following the Semantic Versioning "
    "Specification a breeze.\nIf called with no options, bump will print "
    "the script's current git tag version.",
  prog='keybump',
  usage='%(prog)s [options]',
  formatter_class=RawTextHelpFormatter)
group = parser.add_mutually_exclusive_group()
group.add_argument(
  '-t', '--type', dest='bump_type', type=str, choices=['m', 'n', 'p'],
  help="version bump type:\n"
    "  m = major - x.0.0\n"
    "  n = minor - 1.y.0\n"
    "  p = patch - 1.0.z")
parser.add_argument(
  '-g', '--tag', dest='tag', action='store_true', help='tag git repo with the'
  ' bumped version number')
parser.add_argument(
  '-b', '--build', dest='build', action='store_true', help='build the release'
  ' and upload to the python package index')


def main():
  args = parser.parse_args()

  if args.build:
    build_and_upload()
    info('build released and uploaded..')
    exit(0)

  tags = get_git_tags()
  last_tag = get_git_tag()
  last_version = '0.0.0'
  if len(last_tag) > 0:
    non_decimal = re.compile(r'[^\d.]+')
    last_version = non_decimal.sub('', last_tag)

  if not args.bump_type:
    info('Current tag: %s, version:%s' % (last_tag, last_version))
    exit(0)

  changes = parse_changelog(last_tag, last_version)
  if changes is None:
    fail('Could not parse changelog..')

  # increment the version..
  version, release_date, codename, summaries = changes
  info('version: %s, release_date: %s, codename: %s' % (
    version, release_date, codename))

  new_version = bump_version_num([int(v) for v in version.split('.')], args.bump_type)
  new_release_date = datetime.now().strftime('%Y-%m-%d')
  # setup the dev new version..
  dev_version = new_version + '-dev'

  info('Releasing %s (codename %s, release date %s)',
    new_version, codename, new_release_date)

  if new_version in tags:
    fail('Version "%s" is already tagged', new_version)

  bump_changelog(new_version)
  # set_init_version(new_version)
  # set_setup_version(new_version)
  msg = 'Version bumped to %s' % new_version
  make_git_commit(msg)

  if not git_is_clean():
    fail('You have uncommitted changes in git')

  make_git_tag(msg, new_version)
  # set_init_version(dev_version)
  # set_setup_version(dev_version)

  info(msg)
  exit(0)


if __name__ == '__main__':
  main()
