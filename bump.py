#!/usr/bin/env python

## @file
#  @brief Program description
#  @license GPLv3 or later http://www.gnu.org/licenses/gpl.html
#  @author Reuben Cummings <reubano@gmail.com>

# python imports
from sys import stdout
import argparse
import fileinput

parser = argparse.ArgumentParser(description='template description')
group = parser.add_mutually_exclusive_group()
group.add_argument(
	'-v', '--verbose', dest='verbose', action='store_true', help='increase output verbosity')

group.add_argument(
	'-q', '--quiet', dest='quiet', action='store_true', help='decrease output verbosity')

parser.add_argument(
	'word', dest='word', type=str, default='string', help='just a word')
	
parser.add_argument(
	'square', dest='square', type=int, help='display a square of a given number')

parser.add_argument(
	'-t', '--type', dest='type', type=int, choices=[0, 1, 2], help='the type')
                    
args = parser.parse_args()                    

def main():
	for line in fileinput.input():
	    process(line)
		print "line is %s" % (args.word)
		
# if __name__ == '__main__': main()
