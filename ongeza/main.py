#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

""" An automated way to follow the Semantic Versioning Specification """

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import ongeza

from sys import exit
from os import getcwd, path as p
from argparse import RawTextHelpFormatter, ArgumentParser

from builtins import *
from . import Project, version_is_valid, TRAVIS

CURDIR = None if TRAVIS else p.abspath(getcwd())

parser = ArgumentParser(
    description=(
        "description: ongeza makes following the Semantic Versioning "
        "Specification a breeze.\nIf called with no options, ongeza will "
        "print the current git repository's tag version.\nIf <dir> is not "
        "specified, the current dir is used."),
    prog='ongeza', usage='%(prog)s [options] <dir>',
    formatter_class=RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group()

group.add_argument(
    '-t', '--type', dest='ongeza_type', action='store', metavar='TYPE',
    choices=['m', 'n', 'p', 'major', 'minor', 'patch'],
    help=(
        "version bump type, must be one of:\n"
        "  m or major: [x].0.0\n"
        "  n or minor: x.[y].0\n"
        "  p or patch: x.y.[z]"))

group.add_argument(
    '-s', '--set', dest='new_version', action='store', metavar='VERSION',
    help='set arbitrary version number')

parser.add_argument(
    dest='dir', nargs='?', default=CURDIR,
    help='the project directory (default: %s).\n\n' % CURDIR)

parser.add_argument(
    '-S', '--skip-commit', action='store_true', help='skip committing version'
    ' bumped files')

parser.add_argument(
    '-T', '--tag', action='store_true', help='create git tag at HEAD with the'
    ' bumped version number')

parser.add_argument(
    '-p', '--push', action='store_true', help='push to the remote origin')

parser.add_argument(
    '-a', '--stash', action='store_true', help='stash uncommitted changes')

parser.add_argument(
    '-f', '--tag-format', action='store', metavar='FORMAT',
    default=ongeza.DEFAULT_TAG_FMT, help='git tag format')

parser.add_argument(
    '-F', '--tag-msg-format', action='store', metavar='FORMAT',
    default=ongeza.DEFAULT_TAG_MSG_FMT, help='git tag message format')

parser.add_argument(
    '-c', '--commit-msg-format', action='store', metavar='FORMAT',
    default=ongeza.DEFAULT_COMMIT_MSG_FMT, help='git commit message format')

parser.add_argument(
    '-g', '--sign', action='store_true',
    help='make a GPG-signed tag (implies `--tag`)')

parser.add_argument(
    '-i', '--file', action='store', help='the versioned file')

parser.add_argument(
    '-v', '--version', help="Show version and exit.", action='store_true',
    default=False)

parser.add_argument(
    '-V', '--verbose', action='store_true',
    help='increase output verbosity')

args = parser.parse_args()


def prelim_check(project):
    result = True

    if args.version:
        project.logger.info('ongeza v%s', ongeza.__version__)
    elif project.version and not args.ongeza_type and not args.new_version:
        project.logger.info('Current version: {0.version}'.format(project))
    elif not any([project.version, args.ongeza_type, args.new_version]):
        project.logger.info('No valid versions found.')
    else:
        result = False

    return result


def ongeza_project(project):
    if project.is_dirty and not args.stash:
        error = (
            "Can't bump the version with uncommitted changes. Please "
            "commit your changes or stash the following files and try "
            "again. Optionally, run with '-a' option to auto stash these "
            "files. Dirty files:\n%s" % "\n".join(project.dirty_files))
        raise RuntimeError(error)
    elif project.is_dirty:
        project.logger.info("Stashing changes...\n")
        project.stash()

    if args.new_version and version_is_valid(args.new_version):
        new_version = args.new_version
    elif args.new_version:
        msg = "Invalid version: '{0.version}'. Please use x.y.z format."
        raise RuntimeError(msg.format(args))
    elif project.version and args.ongeza_type:
        new_version = project.ongeza(args.ongeza_type)
    else:
        error = "No git tags found, please run with '-s and -T' options"
        raise RuntimeError(error)

    return new_version


def cleanup(project, new_version):
    msg = "Couldn't find a version to bump."
    if project.bumped and not args.skip_commit:
        message = args.commit_msg_format.format(version=new_version)
        project.add(project.dirty_files)
        project.commit(message)

    if args.stash and project.stash_count:
        project.unstash()

    if project.bumped and (args.tag or args.sign):
        message = args.tag_msg_format.format(version=new_version)
        tag_text = args.tag_format.format(version=new_version)
        project.tag(message, tag_text, sign=args.sign)
    elif args.tag:
        raise RuntimeError("%s Nothing to tag." % msg)

    if project.bumped and args.push:
        project.push()
    elif args.push:
        raise RuntimeError("%s Nothing to push." % msg)


def set_versions(project, new_version):
    # in some cases, e.g., single file python modules, the versioned file
    # can't be predetermined and we must do a 2nd search over all files
    for wave in [1, 2]:
        project.set_versions(new_version, wave)

        if project.bumped:
            msg = 'Bumped from version %s to %s.'
            project.logger.info(msg, project.version, new_version)
            break
    else:
        msg = "Couldn't find version '{0.version}' in any files."
        raise RuntimeError(msg.format(project))


def run():
    project = Project(args.dir, args.file, verbose=args.verbose)

    if prelim_check(project):
        exit(0)

    try:
        new_version = ongeza_project(project)
        set_versions(project, new_version)
    except RuntimeError as err:
        project.logger.error(err)
        exit(1)

    try:
        cleanup(project, new_version)
    except RuntimeError as err:
        project.logger.error(err)
        exit(1)

    exit(0)

if __name__ == "__main__":
    run()
