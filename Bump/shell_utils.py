# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
bump.shell_utils
~~~~~~~~~~~~~~~

helpers for working with the shell.

Examples:
    basic usage::

        >>> sh('echo hello world')
        True
        >>> sh('echo hello world', True)
        'hello world'

Attributes:
    ENCODING (str): The module encoding
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import pygogo as gogo

from subprocess import call, check_output

logger = gogo.Gogo(__name__).logger


def sh(cmd, output=False, path=None):
    """
    runs an external command.

    if the command has a non-zero return code raise a buildfailure. you can pass
    `error=True` to allow non-zero return codes to be allowed to pass silently,
    silently into the night. passing `path="some/path"` will chdir to
    "some/path" before exectuting the command.

        :returns: string of the captured output of the command.
    """
    go = True

    if path:
        try:
            call(['cd', path])
        except OSError:
            logger.error('No such file or directory: %s', path)
            go = False

    if output and go:
        result = check_output(cmd, shell=True).strip()
    elif go:
        result = call(cmd, shell=True) is 0
    elif output:
        result = ''
    else:
        result = False

    return result


def choice(msg):
    """
    prompts for a True/False input from the user command line.

        :returns: boolean for the True/False user response.
    """
    return raw_input("{}  [Yn]: ".format(msg)).lower().startswith('y')
