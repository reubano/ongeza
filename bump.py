#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An automated way to follow the Semantic Versioning Specification """

import os
from sys import exit
from argparse import RawTextHelpFormatter, ArgumentParser
from subprocess import call, check_output

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
		"  m = major - x.0.0\n"
		"  n = minor - 1.y.0\n"
		"  p = patch - 1.0.z")

group.add_argument(
	'-s', '--set', dest='version', action='store',
	help='set arbitrary version number')

parser.add_argument(
	'-v', '--verbose', action='store_true',
	help='increase output verbosity')

parser.add_argument(
	'-g', '--skip-tag', action='store_true', help='skip tagging git repo with '
	'the bumped version number')

parser.add_argument(
	dest='dir', nargs='?', default=os.curdir, type=str,
	help='the project directory')

args = parser.parse_args()

def fail(message, *args):
	print >> stderr(), "error:", message.format(*args)
	exit(1)

def has_tag(git_dir):
	# Check if repo has any git tags.
	if os.path.isdir(git_dir):
		return check_output('cd %s; git tag' % (git_dir), shell=True)
	else:
		raise Exception('%s is not a directory' % (git_dir))

def get_version(git_dir):
	# Get the current release version from git.
	if os.path.isdir(git_dir):
		cmd = 'cd %s; git tag | grep v | tail -n1' % (git_dir)
		version = check_output(cmd, shell=True)
		version = version.lstrip('v').rstrip()
		return version.split('-')[0]
	else:
		raise Exception('%s is not a directory' % (git_dir))

def set_version(old_version, new_version, file, dir, pattern=None):
	if not old_version:
		# find lines in file containing pattern
		cmd = 'cd %s; grep -ine "%s" %s' % (dir, pattern, file)
		lines = check_output(cmd, shell=True)

		# find first line containing a version number
		cmd = 'echo "%s" | grep -im1 "[0-9]*\.[0-9]*\.[0-9]*"' % (lines)
		rep_line = check_output(cmd, shell=True)
		repl_line_num = rep_line.split(':')[0]

		# replace with new version number
		cmd = ("cd %s; sed -i '' '%ss/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s"
			% (dir, repl_line_num, new_version, file))
	else:
		cmd = ("cd %s; sed -i '' 's/%s/%s/g' %s"
			% (dir, old_version, new_version, file))

	return call(cmd, shell=True)

def get_dev_version(version):
	return map(int, version.split('.'))

def git_add(files, git_dir):
	files = ' '.join(files)
	return call('cd %s; git add %s' % (git_dir, files), shell=True)

def git_commit(message, git_dir):
	return call("cd %s; git commit -m '%s'" % (git_dir, message), shell=True)

def git_tag(version, git_dir):
	cmd = ("cd %(g)s; git tag -sm 'Version %(v)s Release' v%(v)s"
		% {'g': git_dir, 'v': version})

	return call(cmd, shell=True)

def bump_version(bump_type, curr_version):
	switch = {
		'm': lambda: [curr_version[0] + 1, 0, 0],
		'n': lambda: [curr_version[0], curr_version[1] + 1, 0],
		'p': lambda: [curr_version[0], curr_version[1], curr_version[2] + 1]}

	return '.'.join(map(str, switch.get(bump_type)()))

def main():
	files = os.listdir(args.dir)
	file_name = ('pearfarm.spec', 'setup.cfg', 'setup.py', )
	file_ext = ('.xml', '.json')
	versioned_files = filter(lambda x: x.endswith(file_ext), files)
	[versioned_files.append(f) for f in files if f in file_name]
	is_tagged = has_tag(args.dir)

	if is_tagged:
		curr_version = get_version(args.dir)
		dev_version = get_dev_version(curr_version)

	if (not is_tagged and args.bump_type):
		fail("No git tags found, please run with the '-s' option")
	elif (is_tagged and not args.bump_type and not args.version):
		string = 'Current version: %s' % curr_version
	elif (is_tagged and args.bump_type):
		new_version = bump_version(args.bump_type, dev_version)
		[set_version(curr_version, new_version, file, args.dir)
			for file in versioned_files]

		string = 'Bump from version %s to %s' % (curr_version, new_version)
	else: # set the version
		# TODO: check args.version validity
		new_version = args.version
		[set_version(None, new_version, file, args.dir)
			for file in versioned_files]

		string = 'Set to version %s' % new_version

	if (args.version or (args.bump_type and is_tagged)):
		message = 'Bump to version %s' % new_version
		git_add(versioned_files, args.dir)
		git_commit(message, args.dir)

	if (not args.skip_tag and version):
		git_tag(version, args.dir)
	elif not args.skip_tag:
		string = "No version found to tag"

	print('%s' % string)

	exit(0)

if __name__ == '__main__':
	main()
