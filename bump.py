#!/usr/bin/env python

""" An automated way to follow the Semantic Versioning Specification """

import os
import re
import logging
import sys
import traceback
import itertools

from argparse import RawTextHelpFormatter
from argparse import ArgumentParser
from subprocess import call
from subprocess import check_output

parser = ArgumentParser(
	description="description: bump makes it easy for you to semantically "
		"version your scripts.\nIf called with no options, bump will print the "
		"script's current git tag version.", prog='bump',
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
		cmd = "echo %s | grep -m1 '[0-9]*\.[0-9]*\.[0-9]*'" % (lines)
		repLine = check_output(cmd, shell=True)
		replLineNum = repLine.split(':')[0]
		
		# replace with new version number
		cmd = ("sed -i '' '%s/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s" 
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
		
	return call(cdm, shell=True)
	
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
		version = getVersion(args.projDir)
		files = os.listdir(args.projDir)
		fileExt = '.spec', '.xml', '.php', '.python'
		versionedFiles = filter(lambda x: x.endswith(fileExt), files)
		
		if args.set:
			pattern = map(getPattern, versionedFiles) # string
			nulls = itertools.repeat(none, len(pattern))
			versions = itertools.repeat(args.set, len(pattern))
			map(setVersion, nulls, versions, versionedFiles, pattern)
			string = ('Set to version %s' % (version))
		elif args.bumpType:
			devVersion = getDevVersion(version)
			newVersion = bumpVersion(args.bumpType, devVersion)
			[setVersion(devVersion, newVersion, file) for file in versionedFiles]
	
			if args.tag:
				gitAdd(versionedFiles, args.projDir)
				gitCommit(message, args.projDir)
				gitTag(newVersion, args.projDir)
			
			string = ('Bump from version %s to %s' % (version, newVersion))
		else: string = ('Current version: %s' % (version))
				
		print('%s' % (string))
	except Exception as err:
		sys.stderr.write('ERROR: %s\n' % str(err))
#		traceback.print_exc(file=sys.stdout)
#		log.exception('%s\n' % str(err))

	sys.exit(0)	

if __name__ == '__main__': main()