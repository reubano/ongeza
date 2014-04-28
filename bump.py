#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An automated way to follow the Semantic Versioning Specification """

import os
from sys import exit
from argparse import RawTextHelpFormatter, ArgumentParser
from Bump import Project, Git


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
	'-S', '--skip-commit', action='store_true', help='skip commiting version'
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
	try:
		project = Project(args.dir)
		git = Git(args.dir)
		cur_version = project.version

		if (not cur_version and args.bump_type):
			raise Exception(
				"No git tags found, please run with '-s and -T' options")
		elif (cur_version and not args.bump_type and not args.version):
			msg = 'Current version: %s' % cur_version
		elif project.is_dirty:
			raise Exception(
				"Can't bump the version with a dirty git index. Please commit "
				"your changes or stash the following files and try again:\n%s" %
				"\n".join(project.dirty_files))
		elif (cur_version and args.bump_type):
			new_version = project.bump(args.bump_type, cur_version)
			project.set_versions(new_version, cur_version)

			if project.bumped:
				msg = 'Bumped from version %s to %s' % (cur_version, new_version)
			else:
				raise Exception("Couldn't find a version to bump.")
		elif args.version:  # set the version
			new_version = args.version
			if not project.check_version(new_version):
				raise Exception(
					"Invalid version: '%s'. Please use x.y.z format." % (
						new_version))
			else:
				project.set_versions(new_version)
				msg = 'Set to version %s' % new_version

		if (project.bumped and not args.skip_commit):
			message = args.commit_format.format(version=new_version)
			git.add(project.versioned_files)
			git.commit(message)

		tag = (project.bumped and args.tag and cur_version)
		tag = (tag or (args.version and args.tag and not cur_version))

		if tag:
			version = (cur_version or args.version)
			message = args.tag_format.format(version=version)
			git.tag(message, version)
		elif args.tag:
			raise Exception("Couldn't find a version to bump. Nothing to tag.")

		if (project.bumped and args.push):
			git.push()
		elif args.push:
			raise Exception("Couldn't find a version to bump. Nothing to push.")

		print(msg)
	except Exception as err:
		print err
		exit(1)

	exit(0)

if __name__ == '__main__':
	main()
