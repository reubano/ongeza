#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An automated way to follow the Semantic Versioning Specification """

import os
from sys import exit
from argparse import RawTextHelpFormatter, ArgumentParser
from subprocess import call, check_output, CalledProcessError

parser = ArgumentParser(
	description="description: bump makes following the Semantic Versioning"
		"Specification a breeze.\nIf called with no options, bump will print "
		"the script's current git tag version.\nIf <dir> is not specified, the "
		"current dir is used", prog='bump',
		usage='%(prog)s [options] <dir>', formatter_class=RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument(
	'-t', '--type', dest='bumpType', type=str, choices=['m', 'n', 'p'],
	help="version bump type:\n"
		"  m = major - x.0.0\n"
		"  n = minor - 1.y.0\n"
		"  p = patch - 1.0.z")

parser.add_argument(
	'-s', '--set', dest='version', action='store', help='set arbitrary version number')

parser.add_argument(
	'-v', '--verbose', dest='verbose', action='store_true',
	help='increase output verbosity')

parser.add_argument(
	'-g', '--tag', dest='tag', action='store_true', help='tag git repo with the'
	' bumped version number')

parser.add_argument(
	dest='dir', nargs='?', default=os.curdir, type=str,
	help='the project directory')

args = parser.parse_args()

def hasTag(gitDir):
	# Check if repo has any git tags.
	if os.path.isdir(gitDir):
		return check_output('cd %s; git tag' % (gitDir), shell=True)
	else:
		raise Exception('%s is not a directory' % (gitDir))

def getVersion(gitDir):
	# Get the current release version from git.
	if os.path.isdir(gitDir):
		cmd = 'cd %s; git tag | grep v | tail -n1' % (gitDir)
		version = check_output(cmd, shell=True)
		version = version.lstrip('v').rstrip()
		return version.split('-')[0]
	else:
		raise Exception('%s is not a directory' % (gitDir))

def setVersion(oldVersion, newVersion, file, dir, pattern=None):
	if not oldVersion:
		# find lines in file containing pattern
		if pattern:
			cmd = 'cd %s; grep -ine "%s" %s' % (dir, pattern, file)
		else:
			cmd = 'cd %s; grep -ine "" %s' % (dir, file)

		try:
			lines = check_output(cmd, shell=True)

			# find first line containing a version number
			cmd = 'echo "%s" | grep -im1 "[0-9]*\.[0-9]*\.[0-9]*"' % (lines)
			repLine = check_output(cmd, shell=True)
			replLineNum = repLine.split(':')[0]
		except CalledProcessError:
			cmd = None
		else:
			# replace with new version number
			cmd = ("cd %s; sed -i '' '%ss/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s"
				% (dir, replLineNum, newVersion, file))
	else:
		cmd = ("cd %s; sed -i '' 's/%s/%s/g' %s"
			% (dir, oldVersion, newVersion, file))

	return call(cmd, shell=True) if cmd else 1

def getDevVersion(version):
	return map(int, version.split('.'))

def gitAdd(files, gitDir):
	files = ' '.join(files)
	return call('cd %s; git add %s' % (gitDir, files), shell=True)

def gitCommit(message, gitDir):
	return call("cd %s; git commit -m '%s'" % (gitDir, message), shell=True)

def gitTag(version, gitDir):
	cmd = ("cd %(g)s; git tag -sm 'Version %(v)s Release' v%(v)s"
		% {'g': gitDir, 'v': version})

	return call(cmd, shell=True)

def bumpVersion(bumpType, currVersion):
	switch = {
		'm': lambda: [currVersion[0] + 1, 0, 0],
		'n': lambda: [currVersion[0], currVersion[1] + 1, 0],
		'p': lambda: [currVersion[0], currVersion[1], currVersion[2] + 1]}

	return '.'.join(map(str, switch.get(bumpType)()))

def main():
	files = os.listdir(args.dir)
	fileName = ('pearfarm.spec', 'setup.cfg', 'setup.py', )
	fileExt = ('.xml', '.json')
	versionedFiles = filter(lambda x: x.endswith(fileExt), files)
	[versionedFiles.append(f) for f in files if f in fileName]
	isTagged = hasTag(args.dir)
	bumped = False

	if isTagged:
		curVersion = getVersion(args.dir)
		devVersion = getDevVersion(curVersion)

	if (not isTagged and args.bumpType):
		string = "No git tags found, please use the '-s' option"
	elif (isTagged and not args.bumpType and not args.version):
		string = 'Current version: %s' % curVersion
	elif (isTagged and args.bumpType):
		newVersion = bumpVersion(args.bumpType, devVersion)
		bumped = [setVersion(curVersion, newVersion, file, args.dir)
			for file in versionedFiles]

		bumped = reduce(lambda x, y: (x == 0) or (y == 0), bumped, 1)

		if bumped:
			string = 'Bump from version %s to %s' % (curVersion, newVersion)
		else:
			string = 'No version found to bump'
	elif args.version: # set the version
		# TODO: check args.version validity
		newVersion = args.version
		bumped = [setVersion(None, newVersion, file, args.dir)
			for file in versionedFiles]

		bumped = reduce(lambda x, y: (x == 0) or (y == 0), bumped, 1)

		if bumped:
			string = 'Set to version %s' % newVersion
		else:
			string = 'No version found to set'
	else:
		string = 'No version found to display'

	if (bumped):
		message = 'Bump to version %s' % newVersion
		gitAdd(versionedFiles, args.dir)
		gitCommit(message, args.dir)

	if (args.tag and newVersion):
		gitTag(newVersion, args.dir)
	elif args.tag:
		string = "No version found to tag"

	print('%s' % string)

	exit(0)

if __name__ == '__main__':
	main()
