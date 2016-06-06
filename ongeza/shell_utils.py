# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
ongeza.shell_utils
~~~~~~~~~~~~~~~~~~

helpers for working with the shell.

Examples:
    basic usage::

        >>> sh('echo hello world')
        True
        >>> sh('echo hello world', True) == 'hello world'
        True

Attributes:
    ENCODING (str): The module encoding
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import os

from subprocess import check_call, check_output, CalledProcessError
from builtins import *

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = False


def quiet_call(cmd, devnull):
    """Calls an external command while suppressing stdout.

    Args:
        cmd (str): The command to run
        devnull (object): File-like object

    Returns:
        bool: True if the commabd return code was zero, else otherwise

    Examples:
        >>> with open(os.devnull, 'wb') as devnull:
        ...     quiet_call('ls', devnull)
        True
    """
    try:
        check_call(cmd, shell=True, stdout=devnull)
    except CalledProcessError:
        return False
    else:
        return True


def sh(cmd, output=False, path=None):
    """runs an external command.

    Args:
        cmd (str): The command to run
        output (bool): return the command output (default: False)
        path (str): The path to run the command from

    Returns:
        mixed: command output if `output` is True, else bool representing
            successful completion of the command

    Examples:
        >>> len(sh('ls', True)) > 0
        True
    """
    good = True

    if path:
        try:
            os.chdir(os.path.abspath(path))
        except OSError:
            good = False

    if output and good:
        try:
            result = check_output(cmd, shell=True).strip().decode('utf-8')
        except CalledProcessError:
            result = ''
    elif good:
        if DEVNULL:
            result = quiet_call(cmd, DEVNULL)
        else:
            with open(os.devnull, 'wb') as devnull:
                result = quiet_call(cmd, devnull)
    elif output:
        result = ''
    else:
        result = False

    return result


def choice(msg):
    """Prompts for a True/False input from the user command line.

    Args:
        msg (str): The message to present to the user

    Returns:
        bool: the user input
    """
    return raw_input("{}  [Yn]: ".format(msg)).lower().startswith('y')
