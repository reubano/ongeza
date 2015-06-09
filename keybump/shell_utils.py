"""
  keybump.shell_utils
  ~~~~~~~~~~~~~~~~~~~

  helpers for the shell.

  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import sys
from logging import getLogger, DEBUG
from sys import exit
from subprocess import Popen
from subprocess import PIPE, STDOUT


__all__ = [
  'sh', 'stderr', 'stdout', 'fail', 'info', 'input', 'choice', 'write',
]


logger = getLogger(__name__)
logger.setLevel(DEBUG)


def sh(command, error=None, cwd=None, *args, **kw):
  """
  runs an external command.

  if the command has a non-zero return code raise a buildfailure. you can pass
  `error=True` to allow non-zero return codes to be allowed to pass silently,
  silently into the night. passing `cwd="some/path"` will chdir to
  "some/path" before exectuting the command.

    :returns: string of the captured output of the command.
  """
  if error is None:
    error = False

  # helpers to auto-format the sh command string..
  if len(args) > 0:
    command = command.format(*args)

  if len(kw) > 0:
    command = command.format(**kw)

  kwargs = {
    'cwd': cwd,
    'shell': True,
    'stderr': STDOUT,
    'stdout': PIPE,
  }

  def run():
    p = Popen(command, **kwargs)
    _stdout, _stderr  = p.communicate()

    if _stdout is not None:
      _stdout = _stdout.decode(sys.getdefaultencoding())

    if _stderr is not None:
      _stderr = _stderr.decode(sys.getdefaultencoding())

    if p.returncode:
      if error:
        fail('''
          command: '{}'
          stdout: {}
          stderr: {}
        ''', command, _stdout, _stderr)

    return _stdout

  return run()


def stderr():
  """
  method to proxy stderr so it can be mocked during tests.
  """
  return sys.stderr


def stdout():
  """
  method to proxy stdout so it can be mocked during tests.
  """
  return sys.stdout


def fail(message, *args):
  logger.error('failure: {}'.format(message))
  if len(args) > 0:
    message = message.format(*args)
  print >> stderr(), "error:", message
  exit(1)


def info(message, *args):
  if len(args) > 0:
    message = str(message).format(*args)
  print >> stdout(), message


def choice(msg):
  """
  prompts for a True/False input from the user command line.

    :returns: boolean for the True/False user response.
  """
  return input("{}  [Yn]: ".format(msg)).upper() in ["Y", "YES", "YE"]


def input(*args, **kw):
  """
  method to proxy `raw_input` so it can be mocked during tests.
  """
  return raw_input(*args, **kw)


def write(path, data):
  """
  write a file.
  """
  with open(path, "w") as f:
    if isinstance(data, basestring):
      f.write(data)
    else:
      f.writelines(data)
