#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manager import Manager
from subprocess import call

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
	"""check style with flake8"""
	cmd1 = 'flake8 --max-complexity=9 --ignore=W191,E126,E128,E203 bump.py'
	cmd2 = 'flake8 --max-complexity=9 --ignore=W191,E126,E128,E203 script'
	cmd = '%s;%s' % (cmd1, cmd2)
	return call(cmd, shell=True)

@manager.command
def test():
	"""Run tests"""
	cmd1 = 'nosetests'
	cmd2 = 'python tests/testscript.py'
	cmd = '%s;%s' % (cmd1, cmd2)
	return call(cmd, shell=True)

if __name__ == '__main__':
	manager.main()
