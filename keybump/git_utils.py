"""
  keybump.git_utils
  ~~~~~~~~~~~~~~~~~

  helpers for working with git.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from keybump.shell_utils import *


__all__ = ['get_current_git_tag', 'get_git_tags', 'get_latest_git_tag',
'git_is_clean', 'git_diff_files', 'git_checkout', 'git_stash', 'make_git_commit',
'make_git_tag', 'push_to_remote', 'ensure_clean_index', 'has_unstaged_changes',
'get_unstaged_files', 'has_uncommitted_changes', 'get_uncommitted_files']


GITHUB_ISSUE_REFERENCE_KEYWORDS = [
  "close",
  "closes",
  "closed",
  "fix",
  "fixes",
  "fixed",
  "resolve",
  "resolves",
  "resolved",
]


COMMIT_PATTERN = r"^(\w*)(\(([\w\$\.\-\* ]*)\))?\: (.*)$"
MAX_SUBJECT_LENGTH = 80


def get_current_git_tag():
  """
    :returns: string of the current git tag on the git index, not the latest
              tag version created.
  """
  return sh("git describe --tags").strip().splitlines()[0]


def get_git_tags():
  """
    :returns: list of git tags, sorted by the date of the commit it points to.
  """
  return sh("git for-each-ref --format='%(tag)' refs/tags").splitlines()


def get_latest_git_tag():
  """
    :returns: list of git tags, sorted by the date of the commit it points to.
  """
  return sh("git describe --tags --abbrev=0").strip()


def git_is_clean():
  """
  returns boolean true/false if there is a dirty index.
  """
  if has_unstaged_changes() or has_uncommitted_changes():
    return False
  else:
    return True
  # return str(sh("git diff --quiet")) == "0"



def has_unstaged_changes():
  return len(sh("git diff-files --ignore-submodules").strip()) > 0

def get_unstaged_files():
  return sh("git diff-files --name-status -r --ignore-submodules")



def has_uncommitted_changes():
  return len(sh("git diff-index --cached HEAD --ignore-submodules").strip()) > 0

def get_uncommitted_files():
  return sh("git diff-index --cached --name-status -r --ignore-submodules HEAD")



def git_diff_files():
  """
    :returns: list of string names of the files that are dirty.
  """
  files = sh("git diff --minimal --numstat")
  return [x.split("\t")[-1] for x in files.splitlines()]


def git_checkout(id):
  """
    :param id: string identifier of the commit'ish to checkout.
  """
  info('checking out: "{}"', id)
  sh("git checkout {}", id)


def git_stash():
  """
  stashes current changes in git.
  """
  sh("git stash")


def get_first_commit():
  """
  returns the first commit with a oneline prettyprint.
  """
  sh("git log --format=\"%H\" --pretty=oneline --reverse")


def get_commits(start, to, format, grep):
  """
  returns list of git commits

    :params start: defaults to the latest git tag.
    :params to: defaults to 'HEAD'
    :params format: defaults to %H%n%s%n%b%n==DEL==
    :params grep: defaults to "feat|^fix|BREAKING"
  """
  if start is None:
    start = get_latest_git_tag()

  if to is None:
    to = 'HEAD'

  if start is not None and len(start) > 0:
    commit_range = "{}..{}".format(start, to)
  else:
    commit_range = ""

  if grep is None:
    grep = "feat|^fix|BREAKING"

  if format is None:
    format = "%H%n%s%n%b%n{}".format(delimiter)

  delimiter = "==DEL=="

  command = "git log --grep=\"^{}\" -E --format='{}' {}".format(
    grep, format, commit_range)

  commits = sh(command).split('\n{}\n'.format(delimiter))
  for commit in commits:
    parse_raw_commit(commit)


def parse_raw_commit(commit):
  """
  parses a raw commit
  """
  # todo
  print 'commit:', commit


def make_git_commit(changelog_file, message):
  """
    :param message: string message for the commit.
  """
  info('making git commit: "{}"', message)
  sh("git add {} && git commit -am {}", changelog_file, message)


def make_git_tag(msg, tag_name):
  """
    :param tag_name: string name for the tag.
  """
  info('making git tag: "{}"', tag_name)
  sh("git tag {} -m {}", tag_name, msg)


def push_to_remote():
  """
  pushes current branch and tags to remote.
  """
  # don't call --all here on purpose..
  sh("git push && git push --tags")


def ensure_clean_index(skip_interactive=False, callback=None):
  """
  ensures the current git staging index has no uncommitted or stashed changes.

    :param skip_interactive: boolean flag to skip getting input from a cli.
    :param callback: recursive callback function.
  """
  if not has_unstaged_changes() and not has_uncommitted_changes():
    if callback:
      return callback(skip_interactive, callback)
    return True

  if callback is None:
    callback = ensure_clean_index

  files = git_diff_files()
  msg = """
  aborting.. un[stashed/committed] changes. fix uncommitted files by
  stashing, committing, or resetting the following files:

  {}
  """.format("\n  ".join(files))
  if skip_interactive:
    fail(msg)

  # clean the index..
  info(msg)
  if not choice("want keybump to snort ..achem stash.. your changes?"):
    fail("aborting.. un[stashed/committed] changes..")

  info("""
  ok, you asked for it..
  """)

  git_stash()

  if callback:
    return callback(skip_interactive, callback)
