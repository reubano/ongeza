#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manager import Manager
from subprocess import call, check_call

manager = Manager()


@manager.command
def clean():
	"""remove Python file artifacts"""
	cmd1 = "find . -name '*.pyc' -exec rm -f {} +"
	cmd2 = "find . -name '*.pyo' -exec rm -f {} +"
	cmd3 = "find . -name '*~' -exec rm -f {} +"
	cmd = '%s;%s;%s' % (cmd1, cmd2, cmd3)
	return call(cmd, shell=True)


@manager.command
def lint():
	"""Check style with flake8"""
	call('flake8', shell=True)


@manager.command
def test():
	"""Run tests"""
	try:
		check_call('nosetests', shell=True) is 0
	except Exception as err:
		raise SystemExit(err)
	else:
		call('python tests/testscript.py', shell=True)


@manager.command
def install():
	"""Build egg"""
	check_call('python setup.py install', shell=True)


if __name__ == '__main__':
	manager.main()
