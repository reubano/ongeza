bump
===========

Introduction
------------

bump makes following the `Semantic Versioning Specification http://semver.org/>`_ a breeze. If called with no options, bump will print the script's current git tag version. It has been tested on the following configuration:

* MacOS X 10.7.4
* Python 2.7.3

Requirements
------------

bump requires the following in order to run properly:

* `Python >= 2.5 <http://www.python.org/download>`_

Preparation
-----------

Check that the correct version of Python is installed

	python -V

Installation (not yet implemented)
------------

Install bump using either pip (recommended)

	sudo pip install bump

or easy_install

	sudo easy_install bump

Using bump
-----------------

Usage
^^^^^

	bump [options] <dir>

Examples
^^^^^^^^

*normal usage*

	bump -tn /path/to/git/repo

*view current version*

	bump /path/to/git/repo

*add tag*

	bump -gtn /path/to/git/repo

*manually set version*

	bump -s 1.0.2  /path/to/git/repo

Options
^^^^^^^

	  -h, --help            show this help message and exit
	  -t {m,n,p}, --type {m,n,p}
							version bump type:
							  m = major - x.0.0
							  n = minor - 1.y.0
							  p = patch - 1.0.z
	  -s SET, --set SET     set arbitrary version number
	  -p PATTERN, --pattern PATTERN
							search pattern when setting arbitrary version number
	  -v, --verbose         increase output verbosity
	  -g, --tag             tag git repo with the bumped version number

Arguments
^^^^^^^^^

+---------+-------------------------------+
| dir     |  the project directory        |
+---------+-------------------------------+

LICENSE
-------

bump is distributed under the `MIT License <http://opensource.org/licenses/mit-license.php>`_, the same as `anotherprogram <http://opensource.org/licenses/alphabetical>`_ on which this program depends.
