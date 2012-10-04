#!/usr/bin/env python

""" An automated way to follow the Semantic Versioning Specification """

import os
import re
import logging
import sys
import traceback
import itertools

from sys import exit
from argparse import RawTextHelpFormatter
from argparse import ArgumentParser
from subprocess import call
from subprocess import check_output

parser = ArgumentParser(
	description="description: bump makes following the Semantic Versioning" "Specification a breeze.\nIf called with no options, bump will print "
		"the script's current git tag version.", prog='bump',
		usage='%(prog)s [options] <dir>', formatter_class=RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument(
	'-t', '--type', dest='bumpType', type=str, choices=['m', 'n', 'p'],
	help="version bump type:\n"
		"  m = major - x.0.0\n"
		"  n = minor - 1.y.0\n"
		"  p = patch - 1.0.z")

group.add_argument(
	'-s', '--set', dest='set', type=str, help='set arbitrary version number')

group.add_argument(
	'-p', '--pattern', dest='pattern', default='version', type=str, help='search pattern when setting arbitrary version number')

parser.add_argument(
	'-v', '--verbose', dest='verbose', action='store_true',
	help='increase output verbosity')

parser.add_argument(
	'-g', '--tag', dest='tag', action='store_true', help='tag git repo with the'
	' bumped version number')

parser.add_argument(dest='projDir', type=str, help='the project directory')

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
		version = check_output(
			'cd %s; git describe --tags' % (gitDir), shell=True)
		version = version.lstrip('v').rstrip()
		return version.split('-')[0]
	else:
		raise Exception('%s is not a directory' % (gitDir))

def setVersion(oldVersion, newVersion, file, pattern=None):
	if not oldVersion:
		# find lines in file containing pattern
		lines = check_output("grep -ne '%s' %s" % (pattern, file), shell=True)

		# find first line containing a version number
		cmd = "echo '%s' | grep -m1 '[0-9]*\.[0-9]*\.[0-9]*'" % (lines)
		repLine = check_output(cmd, shell=True)
		replLineNum = repLine.split(':')[0]

		# replace with new version number
		cmd = ("sed -i '' '%ss/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s"
			% (replLineNum, newVersion, file))
	else:
		cmd = "sed -i '' 's/%s/%s/g' %s" % (oldVersion, newVersion, file)

	return call(cmd, shell=True)

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
	logging.basicConfig(level=logging.WARNING)
	log = logging.getLogger(__name__)

	try:
		files = os.listdir(args.projDir)
		fileExt = '.spec', '.xml', '.cfg'
		versionedFiles = filter(lambda x: x.endswith(fileExt), files)
		isTagged = hasTag(args.projDir)

		if isTagged:
			curVersion = getVersion(args.projDir)
			devVersion = getDevVersion(curVersion)
			newVersion = bumpVersion(args.bumpType, devVersion)
		else:
			newVersion = None

		if (not args.set and not isTagged):
			string = "No git tags found, please use the '-s' option"
		elif (not args.set and not args.bumpType):
			string = 'Current version: %s' % curVersion
		elif args.set:
			[setVersion(None, args.set, file, args.pattern)
				for file in versionedFiles]

			string = 'Set to version %s' % args.set
		else: # it is args.bumpType
			[setVersion(curVersion, newVersion, file)
				for file in versionedFiles]

			string = 'Bump from version %s to %s' % (curVersion, newVersion)

		if args.tag and (args.set or (args.bumpType and isTagged)):
			version = (newVersion or args.set)
			message = 'Bump to version %s' % version
			gitAdd(versionedFiles, args.projDir)
			gitCommit(message, args.projDir)
			gitTag(version, args.projDir)

		print('%s' % (string))
	except Exception as err:
		sys.stderr.write('ERROR: %s\n' % str(err))
#		traceback.print_exc(file=sys.stdout)
#		log.exception('%s\n' % str(err))

	exit(0)

if __name__ == '__main__': main()
