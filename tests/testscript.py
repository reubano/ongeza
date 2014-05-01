#!/usr/bin/env python

""" A script to test bump functionality """

from sys import exit
from scripttest import TestFileEnvironment


def main():
	env = TestFileEnvironment('.scripttest')
	result = env.run('python ../bump.py --help')
	print('%s' % result.stdout)
	exit(0)

if __name__ == '__main__':
	main()
