#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

bump
----

An automated way to follow the Semantic Versioning Specification

"""

__title__ = 'bump'
__package_name__ = 'bump'
__author__ = 'Reuben Cummings'
__description__ = 'An automated way to follow the Semantic Versioning Specification'
__email__ = 'reubano@gmail.com'
__version__ = '0.9.0'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Reuben Cummings'

import os
from subprocess import call, check_output


def sh(cmd, output=False):
	if output:
		return check_output(cmd, shell=True)
	else:
		return call(cmd, shell=True) is 0


class Project(object):
	"""
	class representing a project object.
	"""

	def __init__(self, dir, **kwargs):
		"""
		Parameters
		----------
		dir : str
			the project directory
		"""
		self.current_tag = None
		self.dir = dir

	@property
	def has_tag(self):
		# Check if repo has any git tags.
		if os.path.isdir(self.dir):
			return sh('cd %s; git tag' % (self.dir), True)
		else:
			raise Exception('%s is not a directory' % (self.dir))

	@property
	def versioned_files(self):
		# Get list of files with version metadata.
		files = os.listdir(self.dir)
		file_name = ('pearfarm.spec', 'setup.cfg', 'setup.py', '__init__.py')
		file_ext = ('.xml', '.json')
		versioned_files = filter(lambda x: x.endswith(file_ext), files)
		[versioned_files.append(f) for f in files if f in file_name]
		return versioned_files

	@property
	def version(self):
		# Get the current release version from git.
		if os.path.isdir(self.dir):
			cmd = 'cd %s; git tag | grep v | tail -n1' % (self.dir)
			version = sh(cmd, True)
			version = version.lstrip('v').rstrip()
			return version.split('-')[0]
		else:
			raise Exception('%s is not a directory' % (self.dir))

	@property
	def fmt_version(self):
		# split the version into a list of ints.
		return map(int, self.version.split('.'))

	@property
	def is_clean(self):
		"""
		Returns
		-------
		boolean if there is a dirty index.
		"""
		return sh("cd %s; git diff --quiet" % self.dir)

	@property
	def dirty_files(self):
		"""
		Returns
		-------
		list of string names of the dirty files.
		"""
		files = sh("cd %s; git diff --minimal --numstat" % self.dir, True)
		return [x.split("\t")[-1] for x in files.splitlines()]

	def set_versions(self, new_version, pattern=None, i=0):
		try:
			file = self.versioned_files[i]
			i += 1
		except KeyError:
			return

		if not self.version:
			# find lines in file containing pattern
			cmd = 'cd %s; grep -ine "%s" %s' % (self.dir, pattern, file)
			lines = sh(cmd, True)

			# find first line containing a version number
			cmd = 'echo "%s" | grep -im1 "[0-9]*\.[0-9]*\.[0-9]*"' % (lines)
			rep_line = sh(cmd, True)
			repl_line_num = rep_line.split(':')[0]

			# replace with new version number
			cmd = ("cd %s; sed -i '' '%ss/[0-9]*\.[0-9]*\.[0-9]*/%s/g' %s"
				% (self.dir, repl_line_num, new_version, file))
		else:
			# search for current version number and replace with new version
			# number
			cmd = ("cd %s; sed -i '' 's/%s/%s/g' %s"
				% (self.dir, self.version, new_version, file))

		# TODO: add check to see if any files were changed. Use git.
		sh(cmd)
		return self.set_versions(new_version, pattern, i)

	def check_version(self, new_version):
			cmd = "echo %s | sed 's/[0-9]*\.[0-9]*\.[0-9]*/true/g'" % (
				new_version)
			return sh(cmd, True) is 'true'

	def bump(self, bump_type):
		"""
		Parameters
		----------
		version_num: string version name.
		bump_type: version bump type. one of:
			m = major - [x].0.0
			n = minor - x.[y].0
			p = patch - x.y.[z]
		Returns
		-------
		concatenated string of the incremented version name.
		"""
		version = self.fmt_version

		try:
			switch = {
				'm': lambda: [version[0] + 1, 0, 0],
				'n': lambda: [version[0], version[1] + 1, 0],
				'p': lambda: [version[0], version[1], version[2] + 1]}
		except ValueError:
			raise Exception(
				'Invalid version: %i. Please use x.y.z format.' % self.version)
		else:
			return '.'.join(map(str, switch.get(bump_type)()))


class Git(object):
	"""
	class representing Git commands.
	"""
	def __init__(self, dir):
		"""
		Parameters
		----------
		dir: directory containing the git project
		"""
		self.dir = dir

	def add(self, files):
		files = ' '.join(files)
		return sh('cd %s; git add %s' % (self.dir, files))

	def commit(self, message):
		return sh("cd %s; git commit -m '%s'" % (self.dir, message))

	def tag(self, message, version):
		cmd = "cd %s; git tag -sm '%s' v%s" % (self.dir, message, version)
		return sh(cmd)

	def push(self):
		"""
		pushes current branch and tags to remote.
		"""
		# don't call --all here on purpose..
		return sh("cd %s; git push && git push --tags" % self.dir)
