#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An automated way to follow the Semantic Versioning Specification """

import os
from sys import exit
from argparse import RawTextHelpFormatter, ArgumentParser
from script import Project, Git, fail

parser = ArgumentParser(
	description="description: bump makes following the Semantic Versioning"
		"Specification a breeze.\nIf called with no options, bump will print "
		"the script's current git tag version.\nIf <dir> is not specified, the "
		"current dir is used", prog='bump',
		usage='%(prog)s [options] <dir>', formatter_class=RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument(
	'-t', '--type', dest='bump_type', action='store', choices=['m', 'n', 'p'],
	help="version bump type:\n"
		"  m = major - [x].0.0\n"
		"  n = minor - x.[y].0\n"
		"  p = patch - x.y.[z]")

group.add_argument(
	'-s', '--set', dest='version', action='store',
	help='set arbitrary version number')

parser.add_argument(
	'-v', '--verbose', action='store_true',
	help='increase output verbosity')

parser.add_argument(
	'-c', '--skip-commit', action='store_true', help='skip commiting version '
	' bumped files')

parser.add_argument(
	'-T', '--tag', action='store_true', help='tag git repo with the bumped '
	'version number')

group.add_argument(
	'-p', '--push', action='store_true', help='push to the remote origin')

parser.add_argument(
	'-f', '--tag-format', action='store',
	default='Version {version} Release',
	help='git tag messgae format')

parser.add_argument(
	'-F', '--commit-format', action='store',
	default='Bump to version {version}',
	help='git commit message format')

parser.add_argument(
	dest='dir', nargs='?', default=os.curdir, type=str,
	help='the project directory')

args = parser.parse_args()


def main():
	project = Project()
	git = Git(args.dir)

	files = os.listdir(args.dir)
	file_name = ('pearfarm.spec', 'setup.cfg', 'setup.py', )
	file_ext = ('.xml', '.json')
	versioned_files = filter(lambda x: x.endswith(file_ext), files)
	[versioned_files.append(f) for f in files if f in file_name]

	if (not project.has_tag and args.bump_type):
		fail("No git tags found, please run with the '-s' option")
	elif (project.has_tag and not args.bump_type and not args.version):
		string = 'Current version: %s' % project.version
	elif (project.has_tag and args.bump_type):
		new_version = project.bump_version(args.bump_type)
		[project.set_version(new_version, file) for file in versioned_files]

		string = 'Bump from version %s to %s' % (project.version, new_version)
	else:  # set the version
		# TODO: check args.version validity
		new_version = args.version
		[project.set_version(new_version, file) for file in versioned_files]
		string = 'Set to version %s' % new_version

	if (args.version or (args.bump_type and project.has_tag)):
		message = args.commit_format.format(version=new_version)
		git.add(versioned_files)
		git.commit(message)

	if (args.tag and project.version):
		message = args.tag_format.format(version=project.version)
		git.tag(message, project.version)
	elif args.tag:
		string = "No version found to tag"

	print('%s' % string)

	exit(0)

if __name__ == '__main__':
	main()
